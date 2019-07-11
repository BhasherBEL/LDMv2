_LDMv2_
==

_Abstract_
--
__LDMv2__ (Local Data Mining version 2) is a script written in python that aims to extract a lot of data from a computer.
<p align="center"><img src="https://image.noelshack.com/fichiers/2019/28/4/1562806377-capture.png" alt="Image of LDMv2 project"><p>

It is completely modular in design. That is, a user can write a module without having to understand the rest of the script. This new module will be automatically incorporated into the data recovery process. All its modules are located in the "modules" folder. There are also meta-modules, which aim to simplify the writing of more precise modules. For example, there is a meta module for chromium under Linux, which will search for all user folders. A submodule, such as the one that retrieves cookies, will only have to use it.

It has been designed to be fully portable, and to work, even if all the required dependencies are not present. Each sub-module is executed only if all the dependencies required for its proper functioning are present.

_Requirements_
--
Requirements file coming soon!

_Usages_
--
- Launch with default configuration
```sh
LDMv2.py 
```
- Save outputs in output dir
```sh
LDMv2.py -l1
```
- Display help
```sh
LDMv2.py 
```
Output:
```
usage: LDMv2.py [-h] [-v {0,1,2}] [-l {0,1,2}] [-o OUTPUT]
                [-e [EXECUTE [EXECUTE ...]]] [--html HTML]

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2}, --verbosity {0,1,2}
                        change output verbosity
  -l {0,1,2}, --logtype {0,1,2}
                        change log type
  -o OUTPUT, --output OUTPUT
                        change output dir
  -e [EXECUTE [EXECUTE ...]], --execute [EXECUTE [EXECUTE ...]]
                        set modules to execute
  --html HTML           also generate an html file for data
```

_Supported software_
--

|          | Windows | Linux |
|----------|---------|-------|
| __Browsers__:<br> • Passwords<br> • Cookies<br> • Downloads<br> • History<br> • Saved Data | 7Star<br> Amigo<br> CentBrowser<br> Chedot<br> Chrome SxS<br> Chromium<br> CocCoc<br> Comodo Dragon<br> Elements<br> Epic Privacy<br> Firefox<br> Google Chrome<br> Kometa<br> Opera<br> Orbitum<br> Sputnik<br> Torch<br> Uran<br>  Vivaldi<br> Yandex | Chromium<br> Google Chrome<br> Google Chrome Beta<br> Google Chrome Unstable<br> _~~Opera~~_
| __Network__  | netsh saved networks |       |                                                                                                                                                    

_Contributing_
--
To contribute, see the [contributing file](contributing.md).

You can also follow [this project tab](https://github.com/BhasherBEL/LDMv2/projects/1).

_Thanks_
--
I would like to thank all those who have helped in any way to advance this project
