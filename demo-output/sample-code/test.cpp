
#include <iostream>
#include <vector>

class TestClass {
private:
    int* data;
    int size;
    
public:
    TestClass() {
        // Missing initialization of member variables
        data = NULL;  // Should use nullptr
    }
    
    ~TestClass() {
        delete data;  // Should be delete[]
    }
    
    void process() {
        std::vector<int> v;
        for (int i = 0; i < v.size(); i++) {  // Should use size_t
            v[i] = i;
        }
    }
    
    virtual void virtualFunc() {  // Missing override in derived class
        std::cout << "Base class" << std::endl;
    }
};

class DerivedClass : public TestClass {
public:
    void virtualFunc() {  // Should have override
        std::cout << "Derived class" << std::endl;
    }
};

int main() {
    TestClass* obj = new TestClass();
    obj->process();
    delete obj;
    return 0;
}
