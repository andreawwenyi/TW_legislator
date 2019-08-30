import urllib.request
import argparse
import os
from tqdm import tqdm


def make_url(roc_year, vol, piece, url_skeleton):
    assert(vol > 0), "vol must be greater than 0"
    assert(type(vol) is int), "vol must be an integer"
    
    return url_skeleton.format(year=roc_year, vol=str(vol).zfill(2), piece=str(piece).zfill(2))


def download_single_gazette(pdf_directory, url):
    # filename is the last 6 to 7-digit number + '.pdf' from the url
    file_name = url.split('_')[-1]
    # download the pdf
    urllib.request.urlretrieve(url, os.path.join(pdf_directory, file_name))


def find_max_vol_of_year(url_skeleton, roc_year, v_start, verbose):
    
    # initialization: see if [roc_year] has volume [v_start]
    
    url = make_url(roc_year, v_start, 1, url_skeleton)
    
    try: 
        urllib.request.urlopen(url)
    except urllib.request.HTTPError:
        this_vol_exist = False
        next_move = -1
    else:
        this_vol_exist = True
        next_move = 1

    if verbose:
        print(url, this_vol_exist)
    vol = v_start + next_move
    search_continue = True

    # start to find max volume
    while search_continue:
        prev_vol_exist = this_vol_exist
        url = make_url(roc_year, vol, 1, url_skeleton)
        try: 
            urllib.request.urlopen(url)
        except urllib.request.HTTPError:
            this_vol_exist = False
            next_move = -1
        else:
            this_vol_exist = True
            next_move = 1
        if verbose:
            print(url, this_vol_exist)

        if prev_vol_exist != this_vol_exist:
            search_continue = False
            if prev_vol_exist:  # from exist to not exist
                max_vol = vol-1
            else:
                max_vol = vol
        else:
            vol = vol + next_move
    return max_vol


def main(args):
    url_skeleton = args.url_skl
    pdf_directory = args.pdf_dir
    y = args.year
    v_first = args.v_first
    v_search_start = args.v_search_start
    verbose = args.verbose
    # see if pdf_directory exists; otherwise, create one
    if not os.path.exists(pdf_directory):
        os.mkdir(pdf_directory)

    if args.max_vol: 
        max_vol = args.max_vol
    else:  # if max volume is not specified, search
        print(f'Searching last volume for ROC year {args.year}...')
        max_vol = find_max_vol_of_year(url_skeleton, y, v_search_start, verbose=verbose)
    
    print(f'Last volume for ROC year {args.year} is volume {max_vol}')
    
    v_last = min(args.v_last, max_vol)
    
    for v in tqdm(range(v_first, v_last+1)):
        for p in (1, 2):
            url = make_url(int(y), int(v), int(p), url_skeleton)
            
            if not os.path.isfile(pdf_directory + url.split('_')[-1]):  # if pdf has not been downloaded
                try:  # download pdf
                    download_single_gazette(pdf_directory, url)
                except urllib.request.HTTPError:  # this pdf does not exist
                    pass
                    # print(url, ' does not exist!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url_skl", help="skeleton url",
                        default="https://lci.ly.gov.tw/LyLCEW/communique1/final/pdf/{year}/{vol}/LCIDC01_{year}{vol}{piece}.pdf")
    parser.add_argument("-dir", "--pdf_dir", help="directory to save pdf",
                        default="Data/Gazette/pdfs/")
    
    parser.add_argument("-y", "--year", help="year of document", type=int, default=108)
    parser.add_argument("-vF", "--v_first", help="first volume to collect", type=int, default=1)
    parser.add_argument("-vL", "--v_last", help = "last volume to collect", type=int, default=150)
    parser.add_argument("-vS", "--v_search_start", 
                        help="which v to start with to search max volume of a given year", type=int,
                        default=105)
    parser.add_argument("-maxV", "--max_vol", 
                        help="maximum volume in the year", type=int)
    parser.add_argument("-verbose", "--verbose",
                        help="verbose", action='store_true')
    
    args = parser.parse_args()
    
    main(args)

