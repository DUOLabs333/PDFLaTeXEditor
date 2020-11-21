@echo off

rem This script is part of the TexMaths package
rem http://roland65.free.fr/texmaths
rem
rem Roland Baudin (roland65@free.fr)

rem Process the options
set EXT=%1
set DPI=%2
set TRANS=%3
set TMPPATH=%4
set FILENAME=tmpfile
set COMPILER=%5

rem Convert TMPPATH from URL to path
setlocal enabledelayedexpansion
set TMPPATH=%TMPPATH:file:///=%
set TMPPATH=%TMPPATH:/=\%
set TMPPATH=!TMPPATH:%%20= !
set TMPPATH="%TMPPATH%"

rem Set Paths
set PATH=C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\;%PATH%

rem Generate system log
call :SystemLog

rem Go to the tmp directory
if not %TMPPATH% == "" (
   if not exist %TMPPATH% (
      mkdir %TMPPATH%
   )
	cd /D %TMPPATH%
)

rem Silently remove old files but not the tex file
del /Q *.aux >nul 2>&1
del /Q *.bsl >nul 2>&1
del /Q *.dvi >nul 2>&1
del /Q *.xdv >nul 2>&1
del /Q *.log >nul 2>&1
del /Q *.out >nul 2>&1
del /Q *.dat >nul 2>&1
del /Q *.png >nul 2>&1
del /Q *.svg >nul 2>&1

rem Compile using latex
if "%COMPILER%" == "latex" (

rem Creation of the DVI file
"C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\latex.exe" -shell-escape -interaction=nonstopmode %FILENAME%.tex  > %FILENAME%.out

rem Conversion of the DVI file to a SVG image
if "%EXT%" == "svg" (
   "C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\dvisvgm.exe" -n1 -e %FILENAME%.dvi 2> %FILENAME%.dat
)

rem Conversion of the DVI file to a PNG image
if "%EXT%" == "png" (
if "%TRANS%" == "TRUE" (
   "C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\dvipng.exe" -q -T tight -bg Transparent --width --height --depth -D %DPI% -o %FILENAME%.png %FILENAME%.dvi > %FILENAME%.dat
) else (
   "C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\dvipng.exe" -q -T tight --width --height --depth -D %DPI% -o %FILENAME%.png %FILENAME%.dvi > %FILENAME%.dat
)
)

rem Compile using xelatex
) else (

rem Creation of the XDV file
"C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\xelatex.exe" -no-pdf -shell-escape -interaction=nonstopmode %FILENAME%.tex  > %FILENAME%.out

rem Conversion of the DVI file to a SVG image
"C:\Users\School\Downloads\PDFLaTeXEditor\miktex-portable\texmfs\install\miktex\bin\x64\dvisvgm.exe" -n1 -e %FILENAME%.xdv 2> %FILENAME%.dat
)
Goto :EOF

rem Function used to generate system log
:SystemLog

set SYSLOG=%TMPPATH%..\System.log
rem del %SYSLOG%
for /f "tokens=*" %%a in ('VER') do set VERSION=%%a
echo osType= %VERSION% > %SYSLOG%
echo. >> %SYSLOG%
echo PATH= %PATH% >> %SYSLOG%

Goto :EOF