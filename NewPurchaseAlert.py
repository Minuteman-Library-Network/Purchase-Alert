#!/usr/bin/env python3

"""
Create weekly purhcase alert files in Excel
and upload resulting file to FTP server

Jeremy Goldstein
Minuteman Library Network

Based on code from Gem Stone-Logan
"""

import psycopg2
import xlsxwriter
import os
import pysftp
import configparser
import sys
import time
from datetime import date

#convert sql query results into formatted excel file
def excelWriter(query_results,excelfile):

    #Creating the Excel file for staff
    workbook = xlsxwriter.Workbook(excelfile,{'remove_timezone': True})
    worksheet_adf = workbook.add_worksheet('Adult Fic')
    worksheet_adnf = workbook.add_worksheet('Adult NF')
    worksheet_adlp = workbook.add_worksheet('Large Print')
    worksheet_adunknown = workbook.add_worksheet('Adult Unknown')
    worksheet_adav = workbook.add_worksheet('Adult AV')
    worksheet_j = workbook.add_worksheet('Juv')
    worksheet_ya = workbook.add_worksheet('YA')
    worksheet_other = workbook.add_worksheet('Other')


    #Formatting our Excel worksheet
    worksheet_adf.set_landscape()
    worksheet_adf.hide_gridlines(0)

    #Formatting Cells
    eformat= workbook.add_format({'text_wrap': True, 'valign': 'top'})
    eformatlabel= workbook.add_format({'text_wrap': True, 'valign': 'top', 'bold': True})
    link_format = workbook.add_format({'color': 'blue', 'underline': 1})

    # Setting the column widths
    worksheet_adf.set_column(0,0,14.14)
    worksheet_adf.set_column(1,1,42.43)
    worksheet_adf.set_column(2,2,26.57)
    worksheet_adf.set_column(3,3,10.14)
    worksheet_adf.set_column(4,4,13)
    worksheet_adf.set_column(5,5,9.14)
    worksheet_adf.set_column(6,6,12.71)
    worksheet_adf.set_column(7,7,8.71)
    worksheet_adf.set_column(8,8,12.43)
    worksheet_adf.set_column(9,9,12.71)
    worksheet_adf.set_column(10,10,9.57)
    worksheet_adf.set_column(11,11,22)
    worksheet_adf.set_column(12,12,8.57)
    worksheet_adf.set_column(13,13,12.43)
    worksheet_adf.set_column(14,14,17.14)
    worksheet_adf.set_column(15,15,13.57)
    worksheet_adf.set_column(16,16,45.71)
    worksheet_adnf.set_column(0,0,14.14)
    worksheet_adnf.set_column(1,1,42.43)
    worksheet_adnf.set_column(2,2,26.57)
    worksheet_adnf.set_column(3,3,10.14)
    worksheet_adnf.set_column(4,4,13)
    worksheet_adnf.set_column(5,5,9.14)
    worksheet_adnf.set_column(6,6,12.71)
    worksheet_adnf.set_column(7,7,8.71)
    worksheet_adnf.set_column(8,8,12.43)
    worksheet_adnf.set_column(9,9,12.71)
    worksheet_adnf.set_column(10,10,9.57)
    worksheet_adnf.set_column(11,11,22)
    worksheet_adnf.set_column(12,12,8.57)
    worksheet_adnf.set_column(13,13,12.43)
    worksheet_adnf.set_column(14,14,17.14)
    worksheet_adnf.set_column(15,15,13.57)
    worksheet_adnf.set_column(16,16,45.71)
    worksheet_adlp.set_column(0,0,14.14)
    worksheet_adlp.set_column(1,1,42.43)
    worksheet_adlp.set_column(2,2,26.57)
    worksheet_adlp.set_column(3,3,10.14)
    worksheet_adlp.set_column(4,4,13)
    worksheet_adlp.set_column(5,5,9.14)
    worksheet_adlp.set_column(6,6,12.71)
    worksheet_adlp.set_column(7,7,8.71)
    worksheet_adlp.set_column(8,8,12.43)
    worksheet_adlp.set_column(9,9,12.71)
    worksheet_adlp.set_column(10,10,9.57)
    worksheet_adlp.set_column(11,11,22)
    worksheet_adlp.set_column(12,12,8.57)
    worksheet_adlp.set_column(13,13,12.43)
    worksheet_adlp.set_column(14,14,17.14)
    worksheet_adlp.set_column(15,15,13.57)
    worksheet_adlp.set_column(16,16,45.71)
    worksheet_adunknown.set_column(0,0,14.14)
    worksheet_adunknown.set_column(1,1,42.43)
    worksheet_adunknown.set_column(2,2,26.57)
    worksheet_adunknown.set_column(3,3,10.14)
    worksheet_adunknown.set_column(4,4,13)
    worksheet_adunknown.set_column(5,5,9.14)
    worksheet_adunknown.set_column(6,6,12.71)
    worksheet_adunknown.set_column(7,7,8.71)
    worksheet_adunknown.set_column(8,8,12.43)
    worksheet_adunknown.set_column(9,9,12.71)
    worksheet_adunknown.set_column(10,10,9.57)
    worksheet_adunknown.set_column(11,11,22)
    worksheet_adunknown.set_column(12,12,8.57)
    worksheet_adunknown.set_column(13,13,12.43)
    worksheet_adunknown.set_column(14,14,17.14)
    worksheet_adunknown.set_column(15,15,13.57)
    worksheet_adunknown.set_column(16,16,45.71)
    worksheet_adav.set_column(0,0,14.14)
    worksheet_adav.set_column(1,1,42.43)
    worksheet_adav.set_column(2,2,26.57)
    worksheet_adav.set_column(3,3,10.14)
    worksheet_adav.set_column(4,4,13)
    worksheet_adav.set_column(5,5,9.14)
    worksheet_adav.set_column(6,6,12.71)
    worksheet_adav.set_column(7,7,8.71)
    worksheet_adav.set_column(8,8,12.43)
    worksheet_adav.set_column(9,9,12.71)
    worksheet_adav.set_column(10,10,9.57)
    worksheet_adav.set_column(11,11,22)
    worksheet_adav.set_column(12,12,8.57)
    worksheet_adav.set_column(13,13,12.43)
    worksheet_adav.set_column(14,14,17.14)
    worksheet_adav.set_column(15,15,13.57)
    worksheet_adav.set_column(16,16,45.71)
    worksheet_j.set_column(0,0,14.14)
    worksheet_j.set_column(1,1,42.43)
    worksheet_j.set_column(2,2,26.57)
    worksheet_j.set_column(3,3,10.14)
    worksheet_j.set_column(4,4,13)
    worksheet_j.set_column(5,5,9.14)
    worksheet_j.set_column(6,6,12.71)
    worksheet_j.set_column(7,7,8.71)
    worksheet_j.set_column(8,8,12.43)
    worksheet_j.set_column(9,9,12.71)
    worksheet_j.set_column(10,10,9.57)
    worksheet_j.set_column(11,11,22)
    worksheet_j.set_column(12,12,8.57)
    worksheet_j.set_column(13,13,12.43)
    worksheet_j.set_column(14,14,17.14)
    worksheet_j.set_column(15,15,13.57)
    worksheet_j.set_column(16,16,45.71)
    worksheet_ya.set_column(0,0,14.14)
    worksheet_ya.set_column(1,1,42.43)
    worksheet_ya.set_column(2,2,26.57)
    worksheet_ya.set_column(3,3,10.14)
    worksheet_ya.set_column(4,4,13)
    worksheet_ya.set_column(5,5,9.14)
    worksheet_ya.set_column(6,6,12.71)
    worksheet_ya.set_column(7,7,8.71)
    worksheet_ya.set_column(8,8,12.43)
    worksheet_ya.set_column(9,9,12.71)
    worksheet_ya.set_column(10,10,9.57)
    worksheet_ya.set_column(11,11,22)
    worksheet_ya.set_column(12,12,8.57)
    worksheet_ya.set_column(13,13,12.43)
    worksheet_ya.set_column(14,14,17.14)
    worksheet_ya.set_column(15,15,13.57)
    worksheet_ya.set_column(16,16,45.71)
    worksheet_other.set_column(0,0,14.14)
    worksheet_other.set_column(1,1,42.43)
    worksheet_other.set_column(2,2,26.57)
    worksheet_other.set_column(3,3,10.14)
    worksheet_other.set_column(4,4,13)
    worksheet_other.set_column(5,5,9.14)
    worksheet_other.set_column(6,6,12.71)
    worksheet_other.set_column(7,7,8.71)
    worksheet_other.set_column(8,8,12.43)
    worksheet_other.set_column(9,9,12.71)
    worksheet_other.set_column(10,10,9.57)
    worksheet_other.set_column(11,11,22)
    worksheet_other.set_column(12,12,8.57)
    worksheet_other.set_column(13,13,12.43)
    worksheet_other.set_column(14,14,17.14)
    worksheet_other.set_column(15,15,13.57)
    worksheet_other.set_column(16,16,45.71)

    #Inserting a header
    worksheet_adf.set_header('Purchase Alert')

    # Adding column labels
    worksheet_adf.write(0,0,'Record_number', eformatlabel)
    worksheet_adf.write(0,1,'Title', eformatlabel)
    worksheet_adf.write(0,2,'Author', eformatlabel)
    worksheet_adf.write(0,3,'PublicationYear', eformatlabel)
    worksheet_adf.write(0,4,'MatType', eformatlabel)
    worksheet_adf.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_adf.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_adf.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_adf.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_adf.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_adf.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_adf.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_adf.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_adf.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_adf.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_adf.write(0,15,'OrderLocations', eformatlabel)
    worksheet_adf.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_adnf.write(0,0,'Record_number', eformatlabel)
    worksheet_adnf.write(0,1,'Title', eformatlabel)
    worksheet_adnf.write(0,2,'Author', eformatlabel)
    worksheet_adnf.write(0,3,'PublicationYear', eformatlabel)
    worksheet_adnf.write(0,4,'MatType', eformatlabel)
    worksheet_adnf.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_adnf.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_adnf.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_adnf.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_adnf.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_adnf.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_adnf.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_adnf.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_adnf.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_adnf.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_adnf.write(0,15,'OrderLocations', eformatlabel)
    worksheet_adnf.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_adlp.write(0,0,'Record_number', eformatlabel)
    worksheet_adlp.write(0,1,'Title', eformatlabel)
    worksheet_adlp.write(0,2,'Author', eformatlabel)
    worksheet_adlp.write(0,3,'PublicationYear', eformatlabel)
    worksheet_adlp.write(0,4,'MatType', eformatlabel)
    worksheet_adlp.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_adlp.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_adlp.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_adlp.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_adlp.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_adlp.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_adlp.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_adlp.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_adlp.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_adlp.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_adlp.write(0,15,'OrderLocations', eformatlabel)
    worksheet_adlp.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_adunknown.write(0,0,'Record_number', eformatlabel)
    worksheet_adunknown.write(0,1,'Title', eformatlabel)
    worksheet_adunknown.write(0,2,'Author', eformatlabel)
    worksheet_adunknown.write(0,3,'PublicationYear', eformatlabel)
    worksheet_adunknown.write(0,4,'MatType', eformatlabel)
    worksheet_adunknown.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_adunknown.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_adunknown.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_adunknown.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_adunknown.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_adunknown.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_adunknown.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_adunknown.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_adunknown.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_adunknown.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_adunknown.write(0,15,'OrderLocations', eformatlabel)
    worksheet_adunknown.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_adav.write(0,0,'Record_number', eformatlabel)
    worksheet_adav.write(0,1,'Title', eformatlabel)
    worksheet_adav.write(0,2,'Author', eformatlabel)
    worksheet_adav.write(0,3,'PublicationYear', eformatlabel)
    worksheet_adav.write(0,4,'MatType', eformatlabel)
    worksheet_adav.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_adav.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_adav.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_adav.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_adav.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_adav.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_adav.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_adav.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_adav.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_adav.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_adav.write(0,15,'OrderLocations', eformatlabel)
    worksheet_adav.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_j.write(0,0,'Record_number', eformatlabel)
    worksheet_j.write(0,1,'Title', eformatlabel)
    worksheet_j.write(0,2,'Author', eformatlabel)
    worksheet_j.write(0,3,'PublicationYear', eformatlabel)
    worksheet_j.write(0,4,'MatType', eformatlabel)
    worksheet_j.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_j.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_j.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_j.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_j.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_j.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_j.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_j.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_j.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_j.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_j.write(0,15,'OrderLocations', eformatlabel)
    worksheet_j.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_ya.write(0,0,'Record_number', eformatlabel)
    worksheet_ya.write(0,1,'Title', eformatlabel)
    worksheet_ya.write(0,2,'Author', eformatlabel)
    worksheet_ya.write(0,3,'PublicationYear', eformatlabel)
    worksheet_ya.write(0,4,'MatType', eformatlabel)
    worksheet_ya.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_ya.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_ya.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_ya.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_ya.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_ya.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_ya.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_ya.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_ya.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_ya.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_ya.write(0,15,'OrderLocations', eformatlabel)
    worksheet_ya.write(0,16,'IsbnUPC', eformatlabel)
    worksheet_other.write(0,0,'Record_number', eformatlabel)
    worksheet_other.write(0,1,'Title', eformatlabel)
    worksheet_other.write(0,2,'Author', eformatlabel)
    worksheet_other.write(0,3,'PublicationYear', eformatlabel)
    worksheet_other.write(0,4,'MatType', eformatlabel)
    worksheet_other.write(0,5,'TotalItemCount', eformatlabel)
    worksheet_other.write(0,6,'TotalAvailableItemCount', eformatlabel)
    worksheet_other.write(0,7,'TotalHoldCount', eformatlabel)
    worksheet_other.write(0,8,'TotalDemandRatio', eformatlabel)
    worksheet_other.write(0,9,'LocalAvailableItemCount', eformatlabel)
    worksheet_other.write(0,10,'LocalOrderCopies', eformatlabel)
    worksheet_other.write(0,11,'LocalCopiesInProcess', eformatlabel)
    worksheet_other.write(0,12,'LocalHoldCount', eformatlabel)
    worksheet_other.write(0,13,'LocalDemandRatio', eformatlabel)
    worksheet_other.write(0,14,'SuggestedPurchaseQty (3)', eformatlabel)
    worksheet_other.write(0,15,'OrderLocations', eformatlabel)
    worksheet_other.write(0,16,'IsbnUPC', eformatlabel)

    #initialize row counts at 1 for use with suggested_purchase_formula
    row_adf = 1
    row_adnf = 1
    row_adlp = 1
    row_adunknown = 1
    row_adav = 1
    row_j = 1
    row_ya = 1
    row_other = 1
    # suggested_purchase_formula = '=IF(M2/(VALUE(MID($O$1,SEARCH("(",$O$1)+1,SEARCH(")",$O$1)-SEARCH("(",$O$1)-1)+0))-J2-K2-L2<0,0,ROUND(M2/(VALUE(MID($O$1,SEARCH("(",$O$1)+1,SEARCH(")",$O$1)-SEARCH("(",$O$1)-1)+0))-J2-K2-L2,1))'
    suggested_purchase_formula = '=if(M{}/(VALUE(MID($O$1,SEARCH("(",$O$1)+1,SEARCH(")",$O$1)-SEARCH("(",$O$1)-1)+0))-J{}-K{}-L{}<0,0,round(M{}/(VALUE(MID($O$1,SEARCH("(",$O$1)+1,SEARCH(")",$O$1)-SEARCH("(",$O$1)-1)+0))-J{}-K{}-L{},1))'

    # Writing the report for staff to the Excel worksheet
    for rownum, row in enumerate(query_results):
        #Segment rows out by collection based on format, age level and fiction/non-fiction
        if row[4] == 'LARGE PRINT':
            worksheet_adlp.write(row_adlp,0,row[0], eformat)
            worksheet_adlp.write_url(row_adlp,1,row[13], link_format, row[1])
            worksheet_adlp.write(row_adlp,2,row[2], eformat)
            worksheet_adlp.write(row_adlp,3,row[3], eformat)
            worksheet_adlp.write(row_adlp,4,row[4], eformat)
            worksheet_adlp.write(row_adlp,5,row[5], eformat)
            worksheet_adlp.write(row_adlp,6,row[6], eformat)
            worksheet_adlp.write(row_adlp,7,row[7], eformat)
            worksheet_adlp.write(row_adlp,8,row[8], eformat)
            worksheet_adlp.write(row_adlp,9,row[9], eformat)
            worksheet_adlp.write(row_adlp,10,row[10], eformat)
            worksheet_adlp.write(row_adlp,11,row[18], eformat)
            worksheet_adlp.write(row_adlp,12,row[11], eformat)
            worksheet_adlp.write(row_adlp,13,row[12], eformat)
            worksheet_adlp.write(row_adlp,14,suggested_purchase_formula.format(row_adlp+1,row_adlp+1,row_adlp+1,row_adlp+1,row_adlp+1,row_adlp+1,row_adlp+1,row_adlp+1), eformat)
            worksheet_adlp.write(row_adlp,15,row[14], eformat)
            worksheet_adlp.write(row_adlp,16,row[15], eformat)
            row_adlp += 1
        elif row[16] == 'ADULT' and row[17] == 'TRUE' and row[4] == 'BOOK':
            worksheet_adf.write(row_adf,0,row[0], eformat)
            worksheet_adf.write_url(row_adf,1,row[13], link_format, row[1])
            worksheet_adf.write(row_adf,2,row[2], eformat)
            worksheet_adf.write(row_adf,3,row[3], eformat)
            worksheet_adf.write(row_adf,4,row[4], eformat)
            worksheet_adf.write(row_adf,5,row[5], eformat)
            worksheet_adf.write(row_adf,6,row[6], eformat)
            worksheet_adf.write(row_adf,7,row[7], eformat)
            worksheet_adf.write(row_adf,8,row[8], eformat)
            worksheet_adf.write(row_adf,9,row[9], eformat)
            worksheet_adf.write(row_adf,10,row[10], eformat)
            worksheet_adf.write(row_adf,11,row[18], eformat)
            worksheet_adf.write(row_adf,12,row[11], eformat)
            worksheet_adf.write(row_adf,13,row[12], eformat)
            worksheet_adf.write(row_adf,14,suggested_purchase_formula.format(row_adf+1,row_adf+1,row_adf+1,row_adf+1,row_adf+1,row_adf+1,row_adf+1,row_adf+1), eformat)
            worksheet_adf.write(row_adf,15,row[14], eformat)
            worksheet_adf.write(row_adf,16,row[15], eformat)
            row_adf += 1
        elif row[16] == 'ADULT' and row[17] == 'FALSE' and row[4] in ['BOOK','MUSIC SCORE']:
            worksheet_adnf.write(row_adnf,0,row[0], eformat)
            worksheet_adnf.write_url(row_adnf,1,row[13], link_format, row[1])
            worksheet_adnf.write(row_adnf,2,row[2], eformat)
            worksheet_adnf.write(row_adnf,3,row[3], eformat)
            worksheet_adnf.write(row_adnf,4,row[4], eformat)
            worksheet_adnf.write(row_adnf,5,row[5], eformat)
            worksheet_adnf.write(row_adnf,6,row[6], eformat)
            worksheet_adnf.write(row_adnf,7,row[7], eformat)
            worksheet_adnf.write(row_adnf,8,row[8], eformat)
            worksheet_adnf.write(row_adnf,9,row[9], eformat)
            worksheet_adnf.write(row_adnf,10,row[10], eformat)
            worksheet_adnf.write(row_adnf,11,row[18], eformat)            
            worksheet_adnf.write(row_adnf,12,row[11], eformat)
            worksheet_adnf.write(row_adnf,13,row[12], eformat)
            worksheet_adnf.write(row_adnf,14,suggested_purchase_formula.format(row_adnf+1,row_adnf+1,row_adnf+1,row_adnf+1,row_adnf+1,row_adnf+1,row_adnf+1,row_adnf+1), eformat)
            worksheet_adnf.write(row_adnf,15,row[14], eformat)
            worksheet_adnf.write(row_adnf,16,row[15], eformat)
            row_adnf += 1
        elif row[16] == 'ADULT' and row[17] == 'UNKNOWN' and row[4] in ['BOOK','MUSIC SCORE']:
            worksheet_adunknown.write(row_adunknown,0,row[0], eformat)
            worksheet_adunknown.write_url(row_adunknown,1,row[13], link_format, row[1])
            worksheet_adunknown.write(row_adunknown,2,row[2], eformat)
            worksheet_adunknown.write(row_adunknown,3,row[3], eformat)
            worksheet_adunknown.write(row_adunknown,4,row[4], eformat)
            worksheet_adunknown.write(row_adunknown,5,row[5], eformat)
            worksheet_adunknown.write(row_adunknown,6,row[6], eformat)
            worksheet_adunknown.write(row_adunknown,7,row[7], eformat)
            worksheet_adunknown.write(row_adunknown,8,row[8], eformat)
            worksheet_adunknown.write(row_adunknown,9,row[9], eformat)
            worksheet_adunknown.write(row_adunknown,10,row[10], eformat)
            worksheet_adunknown.write(row_adunknown,11,row[18], eformat)
            worksheet_adunknown.write(row_adunknown,12,row[11], eformat)
            worksheet_adunknown.write(row_adunknown,13,row[12], eformat)
            worksheet_adunknown.write(row_adunknown,14,suggested_purchase_formula.format(row_adunknown+1,row_adunknown+1,row_adunknown+1,row_adunknown+1,row_adunknown+1,row_adunknown+1,row_adunknown+1,row_adunknown+1), eformat)
            worksheet_adunknown.write(row_adunknown,15,row[14], eformat)
            worksheet_adunknown.write(row_adunknown,16,row[15], eformat)
            row_adunknown += 1
        elif row[16] == 'JUV':
            worksheet_j.write(row_j,0,row[0], eformat)
            worksheet_j.write_url(row_j,1,row[13], link_format, row[1])
            worksheet_j.write(row_j,2,row[2], eformat)
            worksheet_j.write(row_j,3,row[3], eformat)
            worksheet_j.write(row_j,4,row[4], eformat)
            worksheet_j.write(row_j,5,row[5], eformat)
            worksheet_j.write(row_j,6,row[6], eformat)
            worksheet_j.write(row_j,7,row[7], eformat)
            worksheet_j.write(row_j,8,row[8], eformat)
            worksheet_j.write(row_j,9,row[9], eformat)
            worksheet_j.write(row_j,10,row[10], eformat)
            worksheet_j.write(row_j,11,row[18], eformat)
            worksheet_j.write(row_j,12,row[11], eformat)
            worksheet_j.write(row_j,13,row[12], eformat)
            worksheet_j.write(row_j,14,suggested_purchase_formula.format(row_j+1,row_j+1,row_j+1,row_j+1,row_j+1,row_j+1,row_j+1,row_j+1), eformat)
            worksheet_j.write(row_j,15,row[14], eformat)
            worksheet_j.write(row_j,16,row[15], eformat)
            row_j += 1
        elif row[16] == 'YA':
            worksheet_ya.write(row_ya,0,row[0], eformat)
            worksheet_ya.write_url(row_ya,1,row[13], link_format, row[1])
            worksheet_ya.write(row_ya,2,row[2], eformat)
            worksheet_ya.write(row_ya,3,row[3], eformat)
            worksheet_ya.write(row_ya,4,row[4], eformat)
            worksheet_ya.write(row_ya,5,row[5], eformat)
            worksheet_ya.write(row_ya,6,row[6], eformat)
            worksheet_ya.write(row_ya,7,row[7], eformat)
            worksheet_ya.write(row_ya,8,row[8], eformat)
            worksheet_ya.write(row_ya,9,row[9], eformat)
            worksheet_ya.write(row_ya,10,row[10], eformat)
            worksheet_ya.write(row_ya,11,row[18], eformat)
            worksheet_ya.write(row_ya,12,row[11], eformat)
            worksheet_ya.write(row_ya,13,row[12], eformat)
            worksheet_ya.write(row_ya,14,suggested_purchase_formula.format(row_ya+1,row_ya+1,row_ya+1,row_ya+1,row_ya+1,row_ya+1,row_ya+1,row_ya+1), eformat)
            worksheet_ya.write(row_ya,15,row[14], eformat)
            worksheet_ya.write(row_ya,16,row[15], eformat)
            row_ya += 1
        elif row[4] == '3-D OBJECT' or row[4] == 'BLU-RAY' or row[4] == 'CONSOLE GAME' or row[4] == 'DVD OR VCD' or row[4] == 'MUSIC CD' or row[4] == 'PLAYAWAY AUDIOBOOK' or row[4] == 'SPOKEN CD':
            worksheet_adav.write(row_adav,0,row[0], eformat)
            worksheet_adav.write_url(row_adav,1,row[13], link_format, row[1])
            worksheet_adav.write(row_adav,2,row[2], eformat)
            worksheet_adav.write(row_adav,3,row[3], eformat)
            worksheet_adav.write(row_adav,4,row[4], eformat)
            worksheet_adav.write(row_adav,5,row[5], eformat)
            worksheet_adav.write(row_adav,6,row[6], eformat)
            worksheet_adav.write(row_adav,7,row[7], eformat)
            worksheet_adav.write(row_adav,8,row[8], eformat)
            worksheet_adav.write(row_adav,9,row[9], eformat)
            worksheet_adav.write(row_adav,10,row[10], eformat)
            worksheet_adav.write(row_adav,11,row[18], eformat)
            worksheet_adav.write(row_adav,12,row[11], eformat)
            worksheet_adav.write(row_adav,13,row[12], eformat)
            worksheet_adav.write(row_adav,14,suggested_purchase_formula.format(row_adav+1,row_adav+1,row_adav+1,row_adav+1,row_adav+1,row_adav+1,row_adav+1,row_adav+1), eformat)
            worksheet_adav.write(row_adav,15,row[14], eformat)
            worksheet_adav.write(row_adav,16,row[15], eformat)
            row_adav += 1
        else:
            worksheet_other.write(row_other,0,row[0], eformat)
            worksheet_other.write_url(row_other,1,row[13], link_format, row[1])
            worksheet_other.write(row_other,2,row[2], eformat)
            worksheet_other.write(row_other,3,row[3], eformat)
            worksheet_other.write(row_other,4,row[4], eformat)
            worksheet_other.write(row_other,5,row[5], eformat)
            worksheet_other.write(row_other,6,row[6], eformat)
            worksheet_other.write(row_other,7,row[7], eformat)
            worksheet_other.write(row_other,8,row[8], eformat)
            worksheet_other.write(row_other,9,row[9], eformat)
            worksheet_other.write(row_other,10,row[10], eformat)
            worksheet_other.write(row_other,11,row[18], eformat)
            worksheet_other.write(row_other,12,row[11], eformat)
            worksheet_other.write(row_other,13,row[12], eformat)
            worksheet_other.write(row_other,14,suggested_purchase_formula.format(row_other+1,row_other+1,row_other+1,row_other+1,row_other+1,row_other+1,row_other+1,row_other+1), eformat)
            worksheet_other.write(row_other,15,row[14], eformat)
            worksheet_other.write(row_other,16,row[15], eformat)
            row_other += 1
    
    workbook.close()
    
    return excelfile

#connect to Sierra-db and store results of an sql query
def runquery(query):

    # import configuration file containing our connection string
    # app.ini looks like the following
    #[db]
    #connection_string = dbname='iii' user='PUT_USERNAME_HERE' host='sierra-db.library-name.org' password='PUT_PASSWORD_HERE' port=1032

    config = configparser.ConfigParser()
    config.read('app_SIC.ini')
      
    try:
	    # variable connection string should be defined in the imported config file
        conn = psycopg2.connect( config['db']['connection_string'] )
    except:
        print("unable to connect to the database")
        clear_connection()
        return
        
    #Opening a session and querying the database for weekly new items
    cursor = conn.cursor()
    cursor.execute(open(query,"r").read())
    #For now, just storing the data in a variable. We'll use it later.
    rows = cursor.fetchall()
    conn.close()
    
    return rows

#upload report to staff ftp server and remove older files
def ftp_file(local_file,library):

    config = configparser.ConfigParser()
    config.read('app_SIC.ini')

    cnopts = pysftp.CnOpts()

    srv = pysftp.Connection(host = config['sic']['sic_host'], username = config['sic']['sic_user'], password= config['sic']['sic_pw'], cnopts=cnopts)

    local_file = local_file

    srv.cwd('/reports/Library-Specific Reports/'+library+'/Purchase Alert/')
    srv.put(local_file)

    #remove old file

    for fname in srv.listdir_attr():
        fullpath = '/reports/Library-Specific Reports/'+library+'/Purchase Alert/{}'.format(fname.filename)
        #time tracked in seconds, st_mtime is time last modified
        name = str(fname.filename)
        #meta.json relates to the user display when accessing the ftp server, and you can safely ignore.
        if (name != 'meta.json') and  ((time.time() - fname.st_mtime) // (24 * 3600) >= 90):
            srv.remove(fullpath)

    srv.close()
    os.remove(local_file)

def main(library,libcode):
	
    tempFile = runquery("NewPurchaseAlert"+libcode+".sql")
    #Name of Excel File
    excelfile =  libcode+'PurchaseAlertNew{}.xlsx'.format(date.today())
    local_file = excelWriter(tempFile,excelfile)
    ftp_file(local_file,library)

#run once for each location
main('Acton','ACT')
main('Acton','AC2')
main('Arlington','ARL')
main('Arlington','AR2')
main('Ashland','ASH')
main('Bedford','BED')
main('Belmont','BLM')
main('Brookline','BRK')
main('Brookline','BR2')
main('Brookline','BR3')
main('Cambridge','CAM')
main('Cambridge','CA3')
main('Cambridge','CA4')
main('Cambridge','CA5')
main('Cambridge','CA6')
main('Cambridge','CA7')
main('Cambridge','CA8')
main('Cambridge','CA9')
main('Concord','CON')
main('Concord','CO2')
main('Concord','CONALL')
main('Dedham','DDM')
main('Dedham','DD2')
main('Dean','DEA')
main('Dover','DOV')
main('Framingham Public','FPL')
main('Framingham Public','FP2')
main('Framingham State','FST')
main('Franklin','FRK')
main('Holliston','HOL')
main('Lasell','LAS')
main('Lexington','LEX')
main('Lincoln','LIN')
main('Maynard','MAY')
main('Medfield','MLD')
main('Medford','MED')
main('Medway','MWY')
main('Millis','MIL')
main('Natick','NAT')
main('Natick','NA2')
main('Needham','NEE')
main('Newton','NTN')
main('Norwood','NOR')
main('Olin','OLN')
main('Regis','REG')
main('Sherborn','SHR')
main('Somerville','SOM')
main('Somerville','SO2')
main('Somerville','SO3')
main('Stow','STO')
main('Sudbury','SUD')
main('Waltham','WLM')
main('Watertown','WAT')
main('Wayland','WYL')
main('Wellesley','WEL')
main('Wellesley','WE2')
main('Wellesley','WE3')
main('Weston','WSN')
main('Westwood','WWD')
main('Westwood','WW2')
main('Winchester','WIN')
main('Woburn','WOB')
