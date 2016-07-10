package main

import (
	"log"
	"time"

	"github.com/ArchieT/trmstac/get"
	"gopkg.in/mgo.v2"
)

func main() {
	session, err := mgo.Dial("127.0.0.1")
	if err != nil {
		panic(err)
	}
	defer session.Close()

	session.SetMode(mgo.Monotonic, true)

	c := session.DB("trmstac").C("allsta")

	waitin := time.NewTimer(time.Duration((15 - (time.Now().Second() % 15)) * 999990000))

	<-waitin.C
	tickin := time.NewTicker(15 * time.Second)

	err = wpis(c)
	if err != nil {
		log.Fatal(err)
	}

	for range tickin.C {
		err = wpis(c)
		if err != nil {
			log.Println(err)
		}
	}
}

func wpis(c *mgo.Collection) (err error) {
	log.Println("start wpis")
	d, err := get.Download()
	log.Println("downloaded")
	if err != nil {
		return
	}
	u, err, err2 := d.ParseAll()
	if err != nil {
		return
	}
	err = err2
	if err != nil {
		return
	}
	a, err := u.Zip()
	if err != nil {
		return
	}
	sh := get.Shot{List: a, Time: d.Time}
	log.Println(sh)
	err = c.Insert(&sh)
	log.Println("insert")
	return
}
