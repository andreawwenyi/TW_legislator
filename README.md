# TW_legislator

Enviornment<br>
python3.6

## download pdfs 下載立院公報
*download_gazette_pdf.py* -- to download the gazette pdfs 

@ Argument:  <br>

Required: <br>
--year: 3 digits of year in ROC 三碼中華民國年份 <br>

Optional: <br> 
--pdf_dir: path to the directory where you want to save this pdf to. Default: Data/Gazette/pdfs. 存pdf的目標資料夾  <br>
--max_vol: total volume of gazettes in the year. 該年度總共公報數，若不知可省略 <br>
--v_search_start: when you don't know the total number of gazettes in the year, specify this variable for the code to search the number of total volume. This is by default set to 105. 若不知該年度總公報數，可設定此一參數以利代碼找尋該年度總公報數。此預設值為105, 為105的總公報數。 <br>
--verbose: if verbose when searching for max volume. 

```
python Code/download_gazette_pdf.py \
--year 107 \
--pdf_dir Data/Gazette/pdfs/107
--verbose \
```

### pdfs to txt 將立院公報PDF檔轉成txt檔

```
pip install pdfminer.six
cd Data/Gazette/pdfs
for a in * ; do pdf2txt.py -o ../txts/${a%.*}.txt $a ; done
```

### txt to lines 將立院公報txt檔整理後轉成list of lines並pickle
```
cd TW_legislator
for a in Data/Gazette/txts/* ; do txt2lines.py -i $a ; done
```
