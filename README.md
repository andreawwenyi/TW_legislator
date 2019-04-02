# TW_legislator

Enviornment<br>
python3.6

## download pdfs 下載立院公報
*download_gazette_pdf.py* -- to download the gazette pdfs 

@ Argument:  <br>

Required: <br>
--pdf_directory: path to the directory where you want to save this pdf to. 存pdf的目標資料夾  <br>
--year: 3 digits of year in ROC 三碼中華民國年份 <br>

Optional: <br> 
--max_vol: total volumne of gazettes in the year. 該年度總共公報數，若不知可省略 <br>
--v_search_start: when you don't know the total number of gazettes in the year, signify this variable for the code to search the number of total volumne. This is by default set to 105. 若不知該年度總公報數，可設定此一參數以利代碼找尋該年度總公報數。此預設值為105, 為105的總公報數。 <br>


```
python3 download_gazette_pdf.py \
--year 105 \
--max_vol 105 \
```

### pdfs to txt 將立院公報PDF檔轉成txt檔

```
pip install pdfminer.six
cd gazette_pdfs
for a in * ; do pdf2txt.py -o ../gazette_txts/${a%.*}.txt $a ; done
```
