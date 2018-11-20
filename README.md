# LED_OCR
OCR for LED

----
### ENVS:
window+py2
no debug under linux

----
### TOOLS:
CV2+MySQL+Flask

----
### Functional:
recognize the characters of trains' number in LED, then check whether they are same with the plans from the Passenger Service System(PST), 
if not alarm from http protocol and insert the information into MySQL DB.

---
### Versions:
There are two versions: one with several files, one with a single file.
The file named LED_Check_singlefile_version is a single file has no relationship with others, it integrate the several functions into one file.
