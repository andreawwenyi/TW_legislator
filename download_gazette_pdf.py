import urllib.request
import argparse
import os
from tqdm import tqdm

def make_url(y, vol, p, url_skeleton):
    assert(vol > 0), "vol must be greater than 0"
    assert(type(vol) is int), "vol must be an integer"
    
    return url_skeleton.format(year = y, vol = str(vol).zfill(2), piece = str(p).zfill(2))

def single_gazette(pdf_directory, url):
    
    #filename is the last 6 to 7 digits number + '.pdf' from the url
    file_name = url.split('_')[-1]
    
    #download the pdf
    urllib.request.urlretrieve(url, pdf_directory + file_name)


def max_vol_of_year(url_skeleton, y, v_start, verbose = False):
    """
    to do: 多找了一次. eg. y = 105, v_start = 107
    """
    
    #initialization
    
    url = make_url(y, v_start, 1, url_skeleton)
    
    try: 
        code = urllib.request.urlopen(url).getcode()
        next_move = 1

    except urllib.request.HTTPError:
        next_move = -1
      
    vol = v_start + next_move
    
    #start to find max volumne
    while True:
        prev_move = next_move
        
        url = make_url(y, vol, 1, url_skeleton)
        
        try: 
            code = urllib.request.urlopen(url).getcode()
            exist = True
        except urllib.request.HTTPError:
            exist = False
        if verbose: print(url, exist)
        
        if exist:
            vol += 1
            next_move = 1
        
        else: 
            if prev_move == 1:
                return vol-1
            
            else:
                vol -= 1
                next_move = -1    


def main(args):
    url_skeleton = args.url_skl
    pdf_directory = args.pdf_dir
    y = args.year
    v_first = args.v_first
    v_search_start = args.v_search_start
    
    
    if args.max_vol: 
        max_vol = args.max_vol
    else: #if max volumne is not passed, search
        max_vol = max_vol_of_year(url_skeleton, y, v_search_start)
    
    print(max_vol)
    
    v_last = min(args.v_last, max_vol)
    
    for v in tqdm(range(v_first,v_last+1)):

        for p in (1,2):
            url = make_url(int(y), int(v), int(p), url_skeleton)
            
            if not os.path.isfile(pdf_directory + url.split('_')[-1]): #if pdf has not been downloaded
                
                try:  #download pdf
                    single_gazette(pdf_directory, url)
                
                except urllib.request.HTTPError: #this pdf does not exist
                    pass
                    #print(url, ' does not exist!')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url_skl", help="skeleton url",
                    default="https://lci.ly.gov.tw/LyLCEW/communique1/final/pdf/{year}/{vol}/LCIDC01_{year}{vol}{piece}.pdf")
    parser.add_argument("-dir", "--pdf_dir", help="directory to save pdf",
                    default="./gazette_pdfs/")
    
    parser.add_argument("-y", "--year", help="year of document", type = int)
    parser.add_argument("-vF", "--v_first", help="first volumne to collect", type = int, default = 1)
    parser.add_argument("-vL", "--v_last", help = "last volumne to collect", type = int, default = 150)
    parser.add_argument("-vS", "--v_search_start", 
                        help = "which v to start with to search max volumne of a given year", type = int, 
                        default = 105)
    parser.add_argument("-maxV", "--max_vol", 
                        help = "maximum volumne in the year", type = int)
    
    args = parser.parse_args()
    
    main(args)

