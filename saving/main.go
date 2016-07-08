package main

import (
	"github.com/ArchieT/trmstac/get"
	"gopkg.in/mgo.v2"
	"log"
	"time"
)

func main() {
	session, err := mgo.Dial("127.0.0.1")
	if err != nil {
		panic(err)
	}
	defer session.Close()

	session.SetMode(mgo.Monotonic, true)

	c := session.DB("trmstac").C("allsta")

	err = wpis(c)
	if err != nil {
		log.Fatal(err)
	}

	tickin := time.NewTicker(20 * time.Second)

	for _ := range tickin.C {
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
