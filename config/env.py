# -*- coding: utf-8 -*- 
## Set Some Const Variables and Basic Exception Message 
import os.path

## Put the Extension Type of a file that you want to read.
ext = ('txt','cpp','hpp','rb')

## If you want to change The Basic Error Message in this library, 
## then You may fetch a new message below on the right side.  
BasicErrorMessage = '예외가 발생했습니다.'

root_dir = os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))) 



