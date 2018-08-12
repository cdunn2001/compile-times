driver:
	python driver.py
go:
	python cogen.py 1021 1000
clean:
	rm -f a.out test_*
