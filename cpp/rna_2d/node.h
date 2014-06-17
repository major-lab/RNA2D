class Node{
    public:
        
        std::vector<int> V;
        void bar(){
            std::cout << "Hello" << std::endl;
        }
        void push(int x){
          V.push_back(x);
        }
        void print(){
            for(int i=0; i<V.size(); i++)
            {
                std::cout << V[i] <<std::endl;
            }
        }
        std::vector<int> get_v()
        {
            return V;
        }
};