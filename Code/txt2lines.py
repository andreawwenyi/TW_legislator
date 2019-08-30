import pickle as pk
import os
import argparse

def txt2lines(path_to_txt, output_dir, pickle = True):
    txt = open(path_to_txt, encoding='utf-8').read()
    txt = txt.replace('\n\n', ' ').replace('\n','')
    txt_lines= txt.split('  ')
    txt_lines = [word for word in txt_lines if word != '']
    
    if pickle:
        #check if output_dir exist; if not, create one
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        
        #pickle file    
        base = os.path.basename(path_to_txt)
        file_name = os.path.splitext(base)[0]+'.pk'
        pk.dump(txt_lines, open(os.path.join(output_dir,file_name), 'wb'))
        return None
    return txt_lines

def main(args):
    txt2lines(args.input_path, args.output_dir, args.pickle)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="path to input txt file")
    parser.add_argument("-o", "--output_dir", help="directory to save output",
                    default="./gazette_lines/")    
    parser.add_argument("-pk", "--pickle", help="if pickle output file", type = bool, default = True)
    args = parser.parse_args()
    main(args)