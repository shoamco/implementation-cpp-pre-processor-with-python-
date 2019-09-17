

enum E_STYLE
{
	E_START,
	E_END
};

int		get_num();
int		get_max(int num1, int num2);
int		get_min(int num1, int num2);
int	    get_sum(int num1, int num2);
int 	factorial(int n);
void 	print_current_time();
void	decorate(E_STYLE style);


int func_of_dummy();
void func_of_iostream();
int factorial(int n)
{
	if (n > 1)
	{
		return(n * factorial(n - 1));
	}
   	else if (n == 1)
   	{	
    	return 1;
   	}
   	else
   	{
		return 0;
	} 
}
