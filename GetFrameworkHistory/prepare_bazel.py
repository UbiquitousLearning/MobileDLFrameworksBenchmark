import os
import re
import traceback

import requests


## From TensorFlow Repo
def convert_version_to_int(version):
    """Convert a version number to a integer that can be used to compare.

  Version strings of the form X.YZ and X.Y.Z-xxxxx are supported. The
  'xxxxx' part, for instance 'homebrew' on OS/X, is ignored.

  Args:
    version: a version to be converted

  Returns:
    An integer if converted successfully, otherwise return None.
  """
    version = version.split('-')[0]
    version_segments = version.split('.')
    for seg in version_segments:
        if not seg.isdigit():
            return None

    version_str = ''.join(['%03d' % int(seg) for seg in version_segments])
    return int(version_str)


def check_bazel_version(min_version, max_version, curr_version) -> bool:
    """Check installed bazel version is between min_version and max_version.

  Args:
    min_version: string for minimum bazel version.
    max_version: string for maximum bazel version.

  Returns:
    The bazel version status.
  """

    min_version_int = convert_version_to_int(min_version)
    curr_version_int = convert_version_to_int(curr_version)
    max_version_int = convert_version_to_int(max_version)

    # Check if current bazel version can be detected properly.

    print('You have bazel %s installed.' % curr_version)

    if curr_version_int < min_version_int:
        print('Please upgrade your bazel installation to version %s or higher to '
              'build TensorFlow!' % min_version)
        return False
    if (curr_version_int > max_version_int and
            'TF_IGNORE_MAX_BAZEL_VERSION' not in os.environ):
        print('Please downgrade your bazel installation to version %s or lower to '
              'build TensorFlow! To downgrade: download the installer for the old '
              'version (from https://github.com/bazelbuild/bazel/releases) then '
              'run the installer.' % max_version)
        return False
    return True


TF_Benchmark_Path = "tensorflow/lite/tools/benchmark"
if not os.path.exists(TF_Benchmark_Path):
    if os.path.exists("tensorflow/contrib/lite/tools/benchmark"):
        TF_Benchmark_Path = "tensorflow/contrib/lite/tools/benchmark"
    else:
        TF_Benchmark_Path = "tensorflow/contrib/lite/tools"
        print("Notice TF Path!")
## FXXK U BAZEL
if os.path.exists(".bazelversion"):
    print("Newest Version!Bye.")
    with open("actions_build.sh", 'w+') as f:
        print(f"bazel build -c opt --config=android_arm64 {TF_Benchmark_Path}:benchmark_model", file=f)
    exit(0)
if not os.path.exists(".bazelrc"):
    with open("actions_build.sh", 'w+') as f:
        print(
            f"bazel build -c opt  --crosstool_top=//external:android/crosstool --host_crosstool_top=@bazel_tools//tools/cpp:toolchain --cpu=arm64-v8a --fat_apk_cpu=arm64-v8a {TF_Benchmark_Path}:benchmark_model",
            file=f)
    with open(".bazelrc", "w+") as f:
        print("import %workspace%/.tf_configure.bazelrc\nimport %workspace%/tools/bazel.rc", file=f)
    content = requests.get("https://x.saltedfish.fun/bazel.rc.old").text
    with open("tools/bazel.rc", "w+") as f:
        f.write(content)

elif not os.path.exists("actions_build.sh"):
    with open("actions_build.sh", 'w+') as f:
        print(
            f"bazel build -c opt  --crosstool_top=//external:android/crosstool --host_crosstool_top=@bazel_tools//tools/cpp:toolchain --cpu=arm64-v8a --fat_apk_cpu=arm64-v8a {TF_Benchmark_Path}:benchmark_model",
            file=f)

if os.path.exists("WORKSPACE"):
    with open("WORKSPACE") as f:
        content = f.readlines()
    for line in content:
        if line.startswith("check_bazel_version_at_least"):
            BAZEL_NUMBER = re.findall(r'check_bazel_version_at_least\("(.+?)"\)', line)[0]
            print("BAZEL VERSION:" + BAZEL_NUMBER)
            with open(".bazelversion", "w+") as f:
                f.write(BAZEL_NUMBER)

if os.path.exists("configure.py"):

    with open("configure.py") as f:
        content = f.readlines()
    for line in content:
        if '_TF_MIN_BAZEL_VERSION' in line:
            BAZEL_NUMBER = re.findall(r"_TF_MIN_BAZEL_VERSION = '(.+?)'", line)[0]
            with open(".bazelversion", "w+") as f:
                f.write(BAZEL_NUMBER)
            break

        if 'check_bazel_version(' in line and 'def' not in line:
            BAZEL_NUMBERs = re.findall(r'check_bazel_version\((.+?)\)', line)
            if len(BAZEL_NUMBERs) == 0:
                continue
            try:
                if ',' in BAZEL_NUMBERs[0]:
                    NUMBERS = BAZEL_NUMBERs[0].split("'")

                    BAZEL_NUMBER_MIN = NUMBERS[1]
                    BAZEL_NUMBER_MAX = NUMBERS[3]
                    print((BAZEL_NUMBER_MAX, BAZEL_NUMBER_MIN, BAZEL_NUMBER))
                    if BAZEL_NUMBER is not None:
                        if check_bazel_version(BAZEL_NUMBER_MIN, BAZEL_NUMBER_MAX, BAZEL_NUMBER):
                            pass
                        else:
                            with open(".bazelversion", "w+") as f:
                                f.write(str(BAZEL_NUMBER_MAX))
                else:
                    NUMBERS = BAZEL_NUMBERs[0].replace("'","")
                    print("BAZEL Version from configure.py:" + NUMBERS)
                    with open(".bazelversion", "w+") as f:
                        f.write(str(NUMBERS))

            except Exception as e:
                print(e)
                # traceback.print_stack()
with open(".bazelversion") as f:
    BAZEL_NUMBER = f.read()
    print(BAZEL_NUMBER)

    try:
        from configure import write_android_ndk_workspace_rule, write_android_sdk_workspace_rule

        write_android_ndk_workspace_rule("/usr/local/lib/android/sdk/ndk-bundle")
        write_android_sdk_workspace_rule("/usr/local/lib/android/sdk", "31.0.0", 21)
    except Exception as e:
        print(e)
        if BAZEL_NUMBER.startswith("0.") and not BAZEL_NUMBER.startswith("0.2"):
            with open("WORKSPACE", "a") as f:
                print('''android_ndk_repository(
  name="androidndk",
  path="/usr/local/lib/android/sdk/ndk-bundle",
  api_level=21)


android_sdk_repository(
  name="androidsdk",
  api_level=31,
  path="/usr/local/lib/android/sdk",
  build_tools_version="31.0.0")''', file=f)
    else:
        print("No Need Write into Workspace")
try:
    res = requests.get(f"https://releases.bazel.build/{BAZEL_NUMBER}/release/bazel-{BAZEL_NUMBER}-linux-x86_64")
    if res.status_code == 404:
        res = requests.get(
            f"https://github.com/bazelbuild/bazel/releases/download/{BAZEL_NUMBER}/bazel-{BAZEL_NUMBER}-installer-linux-x86_64.sh")

        if res.status_code == 404:
            print(f"https://github.com/bazelbuild/bazel/releases/download/{BAZEL_NUMBER}/bazel-{BAZEL_NUMBER}-installer-linux-x86_64.sh 404!")

            BAZEL_NUMBER = "0.14.0"
            with open(".bazelversion", "w+") as f:
                f.write(str(BAZEL_NUMBER))
        else:
            with open('actions_build.sh', 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(
                    f'wget https://github.com/bazelbuild/bazel/releases/download/{BAZEL_NUMBER}/bazel-{BAZEL_NUMBER}-installer-linux-x86_64.sh \nsudo bash bazel-{BAZEL_NUMBER}-installer-linux-x86_64.sh\n' + content)

except Exception as e:
    print(e)
