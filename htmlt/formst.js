function sub()
{
	var password = document.forms["register"]["password"].value;
	var passwordc = document.forms["register"]["passwordc"].value;
	var age = document.forms["register"]["age"].value;
	var dob1 = document.forms["register"]["dob"].value;
	if(password!=passwordc)
	{
		document.getElementById('wpass').innerHTML="Passwords do not match!"
		return false
	}
	if(age>120||age<0)
	{
		document.getElementById('wage').innerHTML="Age Should be greater than 0 and less than 120!"
		return false
	}
	
	
}

