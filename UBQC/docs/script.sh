#!/bin/bash
for i in `seq 21`
	do xelatex im$i.tex
	pdfcrop im$i.pdf
	pdf2svg im$i-crop.pdf im$i.svg
done

#rm -f *.aux *.log *-crop.pdf *.pdf