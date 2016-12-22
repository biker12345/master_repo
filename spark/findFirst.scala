/** Example of polymorphic functions */
object test{
	def findFirst[A](as: Array[A], p: A => Boolean): Int = {
 	@annotation.tailrec
		def loop(n: Int): Int = 
			if (n >= as.length) -1 
			else if (p(as(n))) n 
			else loop(n + 1)

		loop(0)
	}

	def compare (a:Any) : Boolean =
		 if (a==a) true 
		 else false 

	def main(args:Array[String]) : Unit = {
		val x = Array(1,2,3,4,5)
		println(findFirst(x,compare))
	}
}



