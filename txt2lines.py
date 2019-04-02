import pickle as pk
import os

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

def main():
    txt2lines('gazette_txts/1050102.txt', 'gazette_lines', pickle = True)
    
if __name__ == '__main__':
    main()