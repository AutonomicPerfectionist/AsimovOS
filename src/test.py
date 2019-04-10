import threading
import julia
from julia import Main
from julia import Base
from julia.Base import Task

def test(count):
	t = Task(lambda : Main.test_tasks(count))
	Base.schedule(t)
