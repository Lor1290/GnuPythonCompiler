#!/usr/bin/env python3

import time
import sys
import subprocess
from colorama import Fore

class CompTool:

    @staticmethod
    def compile(File: str) -> list:
        Dpos: int = File.index(".")
        
        EFile: str = File[Dpos+1:] 
        NFile: str = File[:Dpos]
        
        result_1: object = ""
        result_2: object  = ""
        
        prog_lang: dict = {
            "py": ["python", f"{File}"],
            "java": ["javac", f"{File}"],
            "f90": ["gfortran", "-o", f"{NFile}", f"{File}"],
            "f95": ["gfortran", "-o", f"{NFile}", f"{File}"],
            "f": ["gfortran", "-o", f"{NFile}", f"{File}"],
            "sh": ["chmod", "+x", f"{File}"],
            "go": ["go", "build", f"{File}"],
            "asm": ["nasm", "-f", "efl64", f"{File}", "-o", f"{NFile}"]
        }

        if EFile not in prog_lang:
            return [None, 2]
        
        proc: object = prog_lang.get(EFile)
        resl: object = subprocess.run(proc, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        if resl.returncode == 0:
            if EFile == "py":
                return [resl.stdout.decode('utf-8').strip(), 0]
            elif EFile == "java":
                resl = subprocess.run(["java", f"{NFile}"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                return [resl.stdout.decode('utf-8').strip(), 0] if resl.returncode == 0 else [resl.stderr.decode('utf-8').strip(), 1]
            elif EFile == "sh":
                resl = subprocess.run([f"./{File}"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
                return [resl.stdout.decode('utf-8').strip(), 0] if resl.returncode == 0 else [resl.stderr.decode('utf-8').strip(), 1]
            else:
                resl = subprocess.run([f"./{NFile}"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                return [resl.stdout.decode('utf-8').strip(), 0] if resl.returncode == 0 else [resl.stderr.decode('utf-8').strip(), 1]
        else:
            return [resl.stderr.decode('utf-8').strip(), 1]


    @staticmethod
    def main() -> int:
        if sys.argv[1:] == []:
            print(Fore.LIGHTRED_EX + "[!] No Input File/s ")
            return 1

        if sys.argv[1:].count("-o"):
            pos_exit: int = sys.argv.index("-o")
            
            if pos_exit == 0 or len(sys.argv[pos_exit+1:]) > 1:
                print(Fore.LIGHTRED_EX + "[!] Invalid Command")
                return 1
    
            file_out: str= "out.txt" if pos_exit == ( len(sys.argv)-1 ) else sys.argv[pos_exit+1]
            with open(file_out, "a+") as file:
                for prog in sys.argv[1:pos_exit]:
                    start = time.time()
                    data = CompTool.compile(prog)
                    end = time.time()

                    if data[1] == 0:
                        file.write(Fore.LIGHTGREEN_EX + f"[+] Program {prog}: \n")
                        file.write(data[0])
                        file.write(Fore.LIGHTGREEN_EX + f"\n[+] Execution time: {end-start:.5f}\n\n")
                    elif data[1] == 2:
                        file.write(Fore.LIGHTYELLOW_EX + f"[!] Extension not found for {prog}!\n")
                    else:
                        file.write(Fore.LIGHTRED_EX + f"[!] Error while parsing {prog}: \n")
                        file.write(f"{data[0]} \n\n")
                return 0

        
        for prog in sys.argv[1:]:
            start = time.time()
            data = CompTool.compile(prog)
            end = time.time()

            if data[1] == 0:
                print(Fore.LIGHTGREEN_EX + f"[+] Program {prog}: \n")
                print(data[0])
                print(Fore.LIGHTGREEN_EX + f"\n[+] Execution time: {end-start:.5f}\n\n")
            elif data[1] == 2:
                print(Fore.LIGHTYELLOW_EX + f"[!] Extension not found!\n")
            else:
                print(Fore.LIGHTRED_EX + f"[!] Error while parsing {prog}: \n")
                print(f"{data[0]} \n\n")

        return 0

if __name__ == '__main__':
    CompTool.main()
