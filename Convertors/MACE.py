#  @Time    : 2021/8/27 上午10:27
#  @Author  : lixiang
#  @FileName: MACE.py
#
#May Shows Error Due to tensorflow issue,just ignore `No module named 'compat' `.
import os
import subprocess

import tensorflow.compat.v1 as tf
import zipfile

# import tensorflow as tf
import  hashlib
import yaml

def CalcFileSha256(filename):
    ''' calculate file sha256 '''
    with open(filename, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
        print(hash_value)
        return hash_value


def MACE(filename):
    template = yaml.load(open('mace_template.yml'))
    model_name = filename.split("/")[-1].split(".")[0]
    template['library_name'] = model_name
    model = template['models']['mobilenet_v1']
    model['model_file_path'] = filename
    model['model_sha256_checksum'] = CalcFileSha256(filename)
    with tf.gfile.GFile(filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def,
                            input_map=None,
                            return_elements=None,
                            name=""
                            )
    # set input output
    op = graph.get_operations()
    inputs = op[0]
    outputs = op[-1]
    input_tensors = []
    input_shapes = []
    output_shapes = []
    output_tensors = []
    for input in inputs.outputs:
        input_tensors.append(input.name.split(':')[0])
        input_shapes.append(",".join(['1' if x is None else str(x) for x in input.shape.as_list()]))
    for output in outputs.outputs:
        output_tensors.append(output.name.split(':')[0])
        output_shapes.append(",".join(['1' if x is None else str(x) for x in output.shape.as_list()]))
    subGraph = {'input_tensors': input_tensors, 'input_shapes': input_shapes, 'output_tensors': output_tensors,
                'output_shapes': output_shapes}
    model['subgraphs'] = [subGraph]
    template['models'] = {model_name: model}
    with open(f"{model_name}.yaml", "w+") as f:
        print(yaml.dump(template), file=f)
    ##!Only TensorFlow 1.X Supported
    # out=subprocess.check_output(f"cd mace-master&& python3 tools/python/convert.py --config ../{model_name}.yaml",shell=True)
    # print(out)
    #
    # f = zipfile.ZipFile(f'./MACE_models/{model_name}.zip', 'w', zipfile.ZIP_DEFLATED)
    # startdir = f"./mace-master/build/{model_name}/model"
    # for dirpath, dirnames, filenames in os.walk(startdir):
    #     for filename in filenames:
    #         f.write(os.path.join(dirpath, filename))
    # f.close()


if __name__ == '__main__':
    filename = "/Users/lixiang/Downloads/frozen_graph.pb"

    MACE(filename)



