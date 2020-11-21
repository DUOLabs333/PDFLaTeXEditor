@echo off

rem This script is part of the TexMaths package
rem http://roland65.free.fr/texmaths
rem
rem Roland Baudin (roland65@free.fr)

rem Process the options
set FILE=%~n1
set TMPPATH=%2

rem Convert TMPPATH from URL to path
setlocal enabledelayedexpansion
set TMPPATH=%TMPPATH:file:///=%
set TMPPATH=%TMPPATH:/=\%
set TMPPATH=!TMPPATH:%%20= !
set TMPPATH="%TMPPATH%"

rem Search path
@for %%e in (%PATHEXT%) do @for %%i in (%FILE%%%e) do @if NOT "%%~$PATH:i"=="" echo %%~$PATH:i > %TMPPATH%
