# pascal-like-interpreter

Language close to Pascal, dynamically compiled in Python.

Example 1 :
```
a := 3 ; b := 4 ;
if (a + b > 5) then {
    print(a+b);
    a := b
} ;
print(a)
```



Example 2 :
```
function syr(n)
{
    while (n != 1) {
        if (n % 2 == 0)
        then {
            n := n / 2
        }
        else {
            n := 3 * n + 1
        };
        print(n)
    } ;
    return n
}
```
