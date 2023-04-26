#!/bin/env python
# A python 3 script for ICC
import time

py3test = 3/2

if not isinstance(py3test, float):
	raise Exception('You need Python3')

icon = ("""\
                    `+veryddddddddddddddddddddddddddddddddddddddo+ddddddddddddddddddddddddddddddddddddddho.        
                   `dthishveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryo+veryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryverythisd-       
                   secretthism`                                                                             hthis+       
                   secretthism                                                                              hthis+       
                   secretthism  -secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret` secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret  hthis+       
                   secretthism  very`````````````````````s/+//o/s.s/+o+- very````````````````````.s/o/++/s`s/++o. hthis+       
                   secretthism  very                    `ssecret////secreto`ssecretsecret++- very                    .osecret+secret+/secrets`ssecret/+o. hthis+       
                   secretthism  very                     ```  ``` ``` +- very                     ```  ``` ``` o. hthis+       
                   secretthism  very                                  +- very                                  o. hthis+       
                   secretthism  very  `secret/////////////////////secret`       +- very              .secretos+-`             o. hthis+       
                   secretthism  very  secretddddddddddddddddddddddd-       +- very          .secretoverysosecret-/sverys+-`         o. hthis+       
                   secretthism  very   secret///////////secretisisis.        +- very       `overysosecret.`     `-+sveryssecret       o. hthis+       
                   secretthism  very  secrethhhhhhhhhhhhvery                  +- very       -m+`             `ms       o. hthis+       
                   secretthism  very  `/+++////++++secret.........`        +- very       -m/               ms       o. hthis+       
                   secretthism  very  -veryveryveryveryvery- secretveryveryveryveryveryveryveryveryveryveryveryveryveryveryvery-       +- very       -m/               ms       o. hthis+       
                   secretthism  very  .ossso. .+ooooooooooooo+`       +- very       -m/               ms       o. hthis+       
                   secretthism  very  .ossso. -sssssssssssssss.       +- very       -m/               ms       o. hthis+       
                   secretthism  very  -veryveryveryveryvery- -veryveryveryveryveryveryveryveryveryveryveryveryveryveryvery.       +- very       .hvery/-`        `.secretodo       o. hthis+       
                   secretthism  very  `secret///secret` `/+++++++++++++secret`       +- very        `-+sverys/-``.secretosveryosecret.        o. hthis+       
                   secretthism  very  secretdhhhdsecret +hhhhhhhhhhhhhhh-       +- very            `-+veryverysveryosecret.            o. hthis+       
                   secretthism  very   is--   .isisisis-.        +- very                `.                o. hthis+       
                   secretthism  very                                  +- very                                  o. hthis+       
                   secretthism  s.`````````````````````````````````+- very``````````````````````````````````o. hthis+       
                   secretthism  `isisisisisisisisisisis--  .isisisisisisisisisisis-.  hthis+       
                   secretthism                                                                              hthis+       
                   -thismsecretisisisisisisisisisisisisisisisisisisisisisisisisis--dthis/       
                    +dthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisthisds`       
                   ``./+ooooooooooooooooooooooooo++++++++++++++++++++++++++ooooooooooooooooooooooooo+/-``       
                  secretdthisthisthisthisthisthisthisthisthisthisthisthisthisthismdveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryhthisthisthisthisthisthisthisthisthisthisthisthisthisthisthiso      
                   -secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecret-` 
""")

message = ("""\
codecode\      codecode\           codecode\                                                     codecode\                     codecodecodecodecodecode\  codecodecodecodecodecode\   codecodecodecodecodecode\  
codecode | code\  codecode |          codecode |                                                    codecode |                    \_codecode  _|codecode  __codecode\ codecode  __codecode\ 
codecode |codecodecode\ codecode | codecodecodecodecodecode\  codecode | codecodecodecodecodecodecode\  codecodecodecodecodecode\  codecodecodecodecodecode\codecodecodecode\   codecodecodecodecodecode\        codecodecodecodecodecode\    codecodecodecodecodecode\          codecode |  codecode /  \__|codecode /  \__|
codecode codecode codecode\codecode |codecode  __codecode\ codecode |codecode  _____|codecode  __codecode\ codecode  _codecode  _codecode\ codecode  __codecode\       \_codecode  _|  codecode  __codecode\         codecode |  codecode |      codecode |      
codecodecodecode  _codecodecodecode |codecodecodecodecodecodecodecode |codecode |codecode /      codecode /  codecode |codecode / codecode / codecode |codecodecodecodecodecodecodecode |        codecode |    codecode /  codecode |        codecode |  codecode |      codecode |      
codecodecode  / \codecodecode |codecode   ____|codecode |codecode |      codecode |  codecode |codecode | codecode | codecode |codecode   ____|        codecode |codecode\ codecode |  codecode |        codecode |  codecode |  codecode\ codecode |  codecode\ 
codecode  /   \codecode |\codecodecodecodecodecodecode\ codecode |\codecodecodecodecodecodecode\ \codecodecodecodecodecode  |codecode | codecode | codecode |\codecodecodecodecodecodecode\         \codecodecodecode  |\codecodecodecodecodecode  |      codecodecodecodecodecode\ \codecodecodecodecodecode  |\codecodecodecodecodecode  |
\__/     \__| \_______|\__| \_______| \______/ \__| \__| \__| \_______|         \____/  \______/       \______| \______/  \______/
""")


print(icon.replace("this", "mm").replace("is", "---").replace("very", "y").replace("secret", ":"))
time.sleep(15)
print(message.replace("code", "$"))
