ssh_enum_v0.3.py
Usage: ssh_enum_v0.3.py [options]

<b>Options<b>:

<pre>
  -h, --help      Show this help message and exit
  
  -u --userlist		Specify a new line delimited username file
  
  -i --ip         Specify the target
  
  -m --multiplier	Specify the multiplier for the password (used to cause the delay)
  
  -t --threshold	Adjust the threshold according to the multipler
  
  -p --port		    Specify a port if the SSH service is not running on port 22
  
  -a --autotune		Calculate the optimum delay/threshold
</pre>


<b>Tips<b>

Running the script with just userlist and host arguments will use defaults. This will work but may not be optimal.

Running the script with autotune will attempt to find the ideal multiplier and appropriate threshold:
ssh_enum_v0.3.py -u users.txt -i 192.168.0.1 -a

After the autotune mode has finished, it will display the multiplier and threshold. These values can be used for subsequent attacks against the same hsot:
ssh_enum_v0.3.py - users.txt -i 192.168.0.1 -m 4000 -t 8
