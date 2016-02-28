# <img src="http://ibarros.com/images/logos/logoWacroSmall.png" width="100"> wacro

String macro operations

wacro is a commandline program that can run multiple string operations
on text files
.

#Commands


syntax: f or find<br>
parameters: takes a find query string as a parameter<br>
description: finds all occurences of a find query and selects them all<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=ll]"
``` 

	1 - selects the ll in the word hello


syntax: r or replace<br>
parameters: takes the string to overwrite selections as parameter<br>
description: replaces all selections with a string<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=ll,r=y]"
```

	1 - selects the ll in the word hello
	2 - replaces them with a y, giving the result "heyo dave"


syntax: ss or start<br>
parameters: takes no parameters<br>
description: This will shrink the selected region to its start position<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=ll,ss,r=y]"
```

	1 - selects the ll in the word hello 
	2 - selects the first l
	3 - replaces the l with a y, giving the result "heylo dave"


syntax: se or end<br>
parameters: takes no parameters<br>
description: This will shrink the selected region to its last position<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=ll,se,r=y]"
```

	1 - selects the ll in the word hello 
	2 - selects the last l
	3 - replaces the l with a y, giving the result "helyo dave"


syntax: ms or move<br>
parameters: takes an amount of postions to move<br>
description: move each selected region by a certain amount. positive numbers go right, negative numbers go left<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=h,ms=1,r=y]"
```

	1 - selects the h in the word hello 
	2 - moves the selected region to now point at the next letter,
		which is the e in the word hello
	3 - replaces the e with a y, giving the result "hyllo dave"


syntax: es or expand<br>
parameters: takes the amount of postions to expand<br>
description: expands the selected region by a certain amount, using postive numbers will expand region, using negative number will contract region<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=ll,es=1,r=i]"
```

	1 - selects the ll in the word hello 
	2 - expands the selected region to now include the e before the ll
		and the o that leads the ll
	3 - replaces the ello with a i, giving the result "hi dave"


syntax: fi or inside<br>
parameters: takes a find query string as a parameter<br>
description:  finds all occurences of a find query in all selected regions and selects them all<br>

examples:
```Batchfile
main.py -i "hello dave" -c "[f=hello,fi=ll,r=y]"
```

	1 - selects the word hello 
	2 - selects the ll in the word hello
	3 - replaces them with a y, giving the result "heyo dave"


syntax: sl or line<br>
parameters: takes no parameters<br>
description: selects the whole line of each selected region<br>

examples:
```Batchfile
main.py -i "hello dave\nhow are things" -c "[f=how,sl,r=sup]"
```

	1 - selects the word how
	2 - selects the whole line where how is located
	3 - replaces the whole line with sup, giving the result "hello dave\nsup"



syntax: ps or print_selection<br>
parameters: takes no parameters<br>
description: prints the current selection to console<br>

examples:
```Batchfile
main.py -i "hello dave\nhow are things" -c "[f=how,ps,sl,ps,r=sup]"
```

	1 - selects the word how
	2 - prints out the word how
	3 - selects the whole line where how is located
	4 - prints out the whole line how are things
	5 - replaces the whole line with sup, giving the result "hello dave\nsup"
