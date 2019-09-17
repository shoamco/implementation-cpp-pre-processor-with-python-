

int get_num()
{
	int num;
   	cout << "Please enter a positive number: ";
	cin >> num;
   
   	return num;
}

int get_max(int num1, int num2)
{
	return  MAX(num1, num2) (num1) > (b) ? (num1) : (b)
);
}

int	get_min(int num1, int num2)
{
	return -( MAX(num1, num2) (num1) > (b) ? (num1) : (b)
) - num1 - num2);
}

int	get_sum(int num1, int num2)
{
	return  SUM(num1, num2) (num1) + (b)
);
}

void decorate(E_STYLE style)
{
	switch (style)
	{
		case E_START:
		{
			cout << "===========   WELCOME   ===========" << endl;
			break;
		}
		case E_END:
		{
			cout << "===========   GOODBYE   ===========" << endl;
			break;
		}
	}
}
