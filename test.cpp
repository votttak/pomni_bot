
#include<iostream>
using namespace std;


//Base class
class Shape {
    public:
        void setWidth(int w) {
            width = w
        }
        void setLength(int l) {
            length = l
        }
        

    protected:
        int width;
        int length;
        
};

//Deribed class
class Rectangle: public Shape {
    public:
        int getArea() {
            return width*length;
        }
};



int main(void) {
    Rectangle Rect;
    Rect.setWidth(5);
    Rect.setWidth(7);

    cout << "Total area: " << Rect.getArea() << endl;
    return 0;
}