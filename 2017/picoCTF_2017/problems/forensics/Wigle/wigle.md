# Connect The Wigle
#### Writeup by intelagent

* **Forensics**
* *140 points*
* Identify the data contained within wigle and determine how to visualize it.

We start by examining what kind of file we are given.

```
$ file wigle
SQLite 3.x database
```

Let's take a look at what is inside the SQLite database. To do this we must start up SQLite3 and tell it which file we want to work with.

```
$ sqlite3
$ .open wigle
$ select * from sqlite_master;

table|android_metadata|android_metadata|2|CREATE TABLE android_metadata (locale text)
table|location|location|3|CREATE TABLE location (_id int, bssid text, level int, lat double, lon double, altitude double, accuracy float, time long)
table|network|network|4|CREATE TABLE network (bssid text, ssid text, frequency int, capabilities text, lasttime long, lastlat double, lastlon double, type text)
```

The table `location` stands out and has the columns `lat` and `long`.

All the values can be extracted.

```
$ select lat,lon from location;
```

We are returned a long list of coordinates in the format of `lat|long`.

We can copy all these coordinates into a file and clean them up with a little python script.

```
fp = open('raw.txt', 'r')
fw = open('formatted.txt', 'w')

for line in fp.readlines():
  fw.write(line.replace('|', ','))
```

We plot these points and the flag becomes visible: `FLAG{f0und_m3_ab70zle2x}`
