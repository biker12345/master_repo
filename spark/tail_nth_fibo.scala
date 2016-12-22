
object FiboObject{
	def fibonaaci(n : Int) : Int = {
		@annotation.tailrec
		def go(n:Int, first:Int,result:Int) : Int = 
			if (n == 0) first
			else go(n-1,result,result=result+first)
		go(n,0,1)
	}

	def main(args:Array[String]) : Unit = {
		println(fibonaaci(6))
	}
}