#!/usr/bin/env python3

import time
import sys, subprocess 
from colorama import Fore


class CompTool:

    @staticmethod
    def compile(File: str) -> list:
        DPos: int = File.index(".")     # -> DotPosition

        FileE: str = File[DPos+1:]      # -> File Extension
        FileN: str = File[:DPos]        # -> File Name

        ProgLang: dict = {
            "py":    f"python {File}",
            "java":  f"java {File}",
            "f":     f"gfortran -o {FileN} {File}",
            "sh":    f"chmod +x {File}", 
            "go":    f"go build {File}",
        }
        
        if FileE not in ProgLang:
            raise("[!] File extension was not found!")
        
        Sequence: list = ProgLang[FileE].split()
        SubProcess = subprocess.run( 
            Sequence, 
            capture_output=True,
            text=True, 
        )
     
        
    @staticmethod    
    def main():
        if sys.argv[1:] == []:
            print(Fore.LIGHTRED_EX + "[!] Not input File/s")
            return 0
        
        for prog in sys.argv[1:]:
            CompTool.compile(prog)
