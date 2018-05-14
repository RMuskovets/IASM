mov 'What do you want to echo?', al
int 5
int 6
pop al
add 'You wrote ', al
pop al
int 5 