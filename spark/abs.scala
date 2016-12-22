/** simple program to implement a abs function using functional programming (pure functions) */

object MyModule{
	
	def abs(n:Int) : Int = 
		if (n < 0 ) -n
		else n


	private def formatAbs(x : Int ) = {
		val msg = "the abs of %d is %d"
		msg.format(x,abs(x))
	}

	def main(args : Array[String] ) : Unit = {
		println(formatAbs(-42))
	}

}