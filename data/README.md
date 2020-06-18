Those data are extracted in order to be tested for outliers in ICMP packets with Dixon-Q test.

For more info about the Dixon-Q test look here and here
https://sebastianraschka.com/Articles/2014_dixon_test.html
http://195.134.76.37/applets/AppletQtest/Appl_Qtest2.html

These data are extracted from cooja, contiki  OS emulator (http://www.contiki-os.org/).
the Number of nodes includes the sink.
All nodes are sending UDP packets to the sink with a PERIOD == 300.
Each node performs a Dixon-Q test on the ICMP packets for each send/receive with a window == 7 (each time the size of previous data to compare).
So every time there is an update on the incoming ICMP packets, the node will perform a test on the last (7) packets to detect outliers.
If an outlier is found, there is a relevant message in the data file.
If both outliers (send/receive) are found for the same time, a "PANIC" message is shown.

The main idea is that if more than two nodes, on the same time show a panic message, the network is under attack.
The probability of both outliers for more than two nodes to exist simultaneously, is zero (no appearance in all tests run for three (3) hours each. Moreover, an attacker must/should/would affect at least five nodes in order for any attack to make sense (Remember, this is an IoT network, even if two or three nodes die, the network should always resume.



