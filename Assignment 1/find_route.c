#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 50
#define ARRAY_SIZE 40

typedef struct Node
{
    struct Node* parent;
    char* node_ID;
    float heuristic;
    float cost;
    char* action;
    struct Node* child;
} Node;

typedef struct Problem
{
    bool informed;
    char* input_filename;
    FILE* ip;
    char* origin_city;
    char* destination_city;
    char* heuristic_filename;
    FILE* hf;
} Problem;

typedef struct Result
{
    bool infinite;
    Node** fringe;
    int fringe_size;
    Node** closed;
    int closed_size;
    int nodesPoped;
    int nodesExpanded;
    int nodesGenerated;
    float distance;


} Result;

/*===Debugging Functions===*/
void printNodeID(char* nodeId);
void nodeCpy(Node* destination, Node* source);
void printNodeInfo(Node* node);
void printNodeArray(int nodeNum, Node** nodeArray);
void rawPrintNodeArray(int array_size, Node** nodeArray);
char* greedyReturnLine(Problem* problem, char* target_city);
float immediateCost(Node* node, Problem* problem);
int howManyLines(Problem* problem);

/*===Utility Functions===*/
float searchHeuristic(char* city, Problem* problem); // Used By: makeNode() and makeInitNode()
int howManyNodes(Node** nodeArray); // Used By: insertSortFringe(), pop(), push(), expand(), insertAll()
void freeNodeArray(int array_size, Node** nodeArray); // Used By: main()
void incrementFringeSize(int* fringe_size, Node*** Fringe); // Used By: push()
Node* makeNode(char* childName, Problem* problem); // Used By: successorFn()
Node* makeInitNode(Problem* problem); // Used By: initFringe()
void insertSortFringe(Node** fringe, Problem* problem); // Used By: insertAll()
bool searchClosed(Node** closed, int closed_size, Node* node ); // Used By: graphSearch()
void push(int* fringe_size, Node* node, Node*** fringe); // Used By: successorFn(), initFringe(), expand(), insertAll(), graphSearch()

/*===Search Functions===*/
Node* pop(Node*** fringe); // implements REMOVE-FRONT()
Node** successorFn(Problem* problem, Node* node); // implements SUCCESSOR-FN()
float stepCost(Node* node, Node* s, Problem* problem); // implements STEP-COST()
Node** initFringe(int* fringe_size, Problem* problem); // implements INSERT(MAKE-NODE()) [e.g. It implements both INSERT() and MAKE-NODE() by calling makeInitNode() within initFringe definition]
Node* goalTest(Problem* problem, Node* node); // implements GOAL-TEST()
Node** expand(Problem* problem, Node* node, Result* result); // implements EXPAND()
void insertAll(Node** successors, Node*** fringe, int* fringe_size, Problem* problem); // implements INSERTALL()
Node* graphSearch(Problem* problem, Result* result); // implements GRAPH-SEARCH()

/*===Prints the Optimal Route===*/
void printRoute(Node* node, Problem* problem);

int main(int argc, char *argv[])
{
    if(argc == 4) //we are doing unformed search
    { 
        char* input_filename = argv[1];
        char* origin_city = argv[2];
        char* destination_city = argv[3];

        FILE* fp;
        fp = fopen(input_filename, "r");
        if(fp == NULL)
        {
            perror("Error opening file");
            return 1;
        }

        Problem* problem = calloc(1, sizeof(Problem));
        problem->informed = false;
        problem->input_filename = input_filename;
        problem->ip = fp;
        problem->origin_city = origin_city;
        problem->destination_city = destination_city;
        problem->heuristic_filename = NULL;
        problem->hf = NULL;

        Result* result = calloc(1,sizeof(Result));
        result->infinite = false;
        result->fringe = NULL;
        result->fringe_size = 0;
        result->closed = NULL;
        result->closed_size = 0;
        result->nodesPoped = 0;
        result->nodesExpanded = 0;
        result->nodesGenerated = 0;
        result->distance = 0.0;

        Node* destination = graphSearch(problem, result);

        printf("Nodes Popped: %d\n",result->nodesPoped);
        printf("Nodes Expanded: %d\n",result->nodesExpanded);
        printf("Nodes Generated: %d\n",result->nodesGenerated);
        if(result->infinite == true)
        {
            printf("Distance: infinity\n");
            printf("Route:\nNone\n");
        } 
        else if(result->infinite == false)
        {
            printf("Distance: %.1f km\n",result->distance);
            printRoute(destination, problem);           
        } 
        if(destination != NULL)
        {
            free(destination->node_ID);
            free(destination->action);
            free(destination);
        }

        freeNodeArray(result->fringe_size, result->fringe);
        freeNodeArray(result->closed_size, result->closed);
        free(result->fringe);
        free(result->closed);
        free(problem);
        free(result);
        rewind(fp);
        fclose(fp);
    }
    else if(argc == 5) //we are doing informed search
    { 
        char* input_filename = argv[1];
        char* origin_city = argv[2];
        char* destination_city = argv[3];
        char* heuristic_filename = argv[4];


        FILE* fp;
        fp = fopen(input_filename, "r");
        if(fp == NULL)
        {
            perror("Error opening file");
            return 1;
        }
        FILE* hf;
        hf = fopen(heuristic_filename, "r");
        if(hf == NULL)
        {
            perror("Error opening file");
            return 1;
        }

        Problem* problem = calloc(1, sizeof(Problem));
        problem->informed = true;
        problem->input_filename = input_filename;
        problem->ip = fp;
        problem->origin_city = origin_city;
        problem->destination_city = destination_city;
        problem->heuristic_filename = heuristic_filename;
        problem->hf = hf;

        Result* result = calloc(1,sizeof(Result));
        result->infinite = false;
        result->fringe = NULL;
        result->fringe_size = 0;
        result->closed = NULL;
        result->closed_size = 0;
        result->nodesPoped = 0;
        result->nodesExpanded = 0;
        result->nodesGenerated = 0;
        result->distance = 0.0;

        Node* destination = graphSearch(problem, result);

        printf("Nodes Popped: %d\n",result->nodesPoped);
        printf("Nodes Expanded: %d\n",result->nodesExpanded);
        printf("Nodes Generated: %d\n",result->nodesGenerated);
        if(result->infinite == true)
        {
            printf("Distance: infinity\n");
            printf("Route:\nNone\n");
        } 
        else if(result->infinite == false)
        {
            printf("Distance: %.1f km\n",result->distance);
            printRoute(destination, problem);           
        } 
        if(destination != NULL)
        {
            free(destination->node_ID);
            free(destination->action);
            free(destination);
        }

        freeNodeArray(result->fringe_size, result->fringe);
        freeNodeArray(result->closed_size, result->closed);
        free(result->fringe);
        free(result->closed);
        free(problem);
        free(result);
        rewind(fp);
        rewind(hf);
        fclose(hf);
        fclose(fp);
        
    }

    return 0;
}

void printNodeID(char* nodeId)
{
    printf("%s",nodeId);
}

void nodeCpy(Node* destination, Node* source)
{
    destination->parent = source->parent;
    destination->node_ID = source->node_ID;
    destination->heuristic = source->heuristic;
    destination->cost = source->cost;
    destination->action = source->action;
    destination->child = source->child;

}

void printNodeInfo(Node* node)
{
    // parent
    if(node->parent == NULL) printf("\n(Parent Node: NULL| ");
    else printf("\n(Parent Node: %s[%p]| ",(node->parent)->node_ID,node->parent);
    // node_ID
    printf("Node_ID: %s| ",node->node_ID);
    // heuristic
    printf("heuristic: %1.f| ",node->heuristic);
    // int cost
    printf("cost: %1.f| ",node->cost);
    // action
    printf("action: %s| ",node->action);

    // child;
    if(node->child == NULL) printf("Child Node: NULL)\n");
    else printf("Child Node: %s[%p])\n",(node->child)->node_ID,node->child);
}

void printNodeArray(int nodeNum, Node** nodeArray)
{
    if(nodeNum == 0 || nodeArray == NULL)
    {
        printf("nodeNum is zero\n");
        return;
    } 
    int i;
    for(i = 0; i<nodeNum; i++) 
    {
        if(i!=nodeNum-1)
        {
            printf("(");printNodeID(nodeArray[i]->node_ID);printf(", Cost: %1.f, Heuristic: %1.f, f(n): %1.f",nodeArray[i]->cost,nodeArray[i]->heuristic,nodeArray[i]->cost+nodeArray[i]->heuristic); printf(")");
            printf(" | ");
        }
        else if(i==nodeNum-1)
        {
            printf("(");printNodeID(nodeArray[i]->node_ID);printf(", Cost: %1.f, Heuristic: %1.f, f(n): %1.f",nodeArray[i]->cost,nodeArray[i]->heuristic,nodeArray[i]->cost+nodeArray[i]->heuristic); printf(")");
            printf("|\n");
        }
    }
    i = 0;
    return;
}

void rawPrintNodeArray(int array_size, Node** nodeArray)
{
    int i;
    for(i = 0; i<array_size; i++) 
    {
        if(nodeArray[i]!=0)
        {
            printf("(Node: ");
            printNodeID(nodeArray[i]->node_ID);
            printf(", Action: "); printNodeID(nodeArray[i]->action);
            printf(", Cost:%f",nodeArray[i]->cost);
            printf(")| ");
        }
        else if(nodeArray[i]==0 && i!=array_size-1) printf("0 | ");
        else if(nodeArray[i]==0 && i==array_size-1) printf("0\n");
    }
    i = 0;
    return;
}

char* greedyReturnLine(Problem* problem, char* target_city) //returns the first match in the input file
{
    char* line = calloc(MAX_LINE_LENGTH,sizeof(char));

    char tmp[MAX_LINE_LENGTH];
    char buffer[MAX_LINE_LENGTH];
    memset(tmp,'\0',sizeof(tmp));
    memset(buffer,'\0',sizeof(buffer));

    char* token = NULL;
    while(fgets(buffer,sizeof(buffer),problem->ip) != NULL)
    {
        strcpy(tmp,buffer);
        // Time to parse the buffer and see if we've found the target line
        if(line[0]=='\0') //we havent found our origin city
        {
            token = strtok(buffer," ");
            if(strcmp(token,target_city)==0) //if we find our target we want to save it to the buffer for good and let the loop finish out
            {
                strcpy(line,tmp);
            }
            memset(buffer, '\0',sizeof(buffer));
            memset(tmp, '\0',sizeof(tmp));
            token = NULL;
        }
    }
    rewind(problem->ip);
    return line;

}

float immediateCost(Node* node, Problem* problem)
{
    float cost = 0.0;
    char buffer[MAX_LINE_LENGTH];
    memset(buffer,'\0',sizeof(buffer));
    
    char* token = NULL;
    while(fgets(buffer, sizeof(buffer),problem->ip) != NULL)
    {
        token = strtok(buffer," "); //gets the first element from each line in the file
        if(strcmp(token,node->node_ID) == 0 && strcmp(token,"END") != 0) // we found a child
        {
            token = strtok(NULL," "); // gets the name of the child
            // printf("[node->action: %s]\n",node->action);
            if(strcmp(token,node->action) == 0 && strcmp(token,"END") != 0)
            {
                token = strtok(NULL," ");
                cost = atof(token);
                
            }
        }
        token = NULL;
        memset(buffer,'\0',sizeof(buffer));
    }
    rewind(problem->ip);
    return cost;
}

int howManyLines(Problem* problem) // returns the total number of lines in the file
{
    int count = 0;
    char buffer[MAX_LINE_LENGTH];
    memset(buffer,'\0',sizeof(buffer));

    while(fgets(buffer,sizeof(buffer),problem->ip) != NULL)
    {
        count++;
        memset(buffer, '\0',sizeof(buffer));
    }
    rewind(problem->ip);
    return count;
}

float searchHeuristic(char* city, Problem* problem) //returns the heuristic of a given city
{
    float heuristic = 0.0;
    char buffer[MAX_LINE_LENGTH];
    memset(buffer,'\0',sizeof(buffer));
    
    char* token = NULL;
    char* lineArgs[2] = {};

    while(fgets(buffer, sizeof(buffer),problem->hf) != NULL)
    {
        token = strtok(buffer," "); //gets the first element from each line in the file
        lineArgs[0] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[0],token);

        token = strtok(NULL," "); //gets the second element from each line in the file
        lineArgs[1] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[1],token);

        token = NULL;

        if((strcmp(city,lineArgs[0]) == 0 && (strcmp(lineArgs[0],"END")!=0 || strcmp(lineArgs[0],"OF")!=0 || strcmp(lineArgs[0],"INPUT")!=0))) //We found the heuristic for the given city
        {
            heuristic = atof(lineArgs[1]); // we found the heuristic
        }
        free(lineArgs[0]);
        free(lineArgs[1]);
        memset(buffer,'\0',sizeof(buffer));
    }
    rewind(problem->hf);
    return heuristic;
}

int howManyNodes(Node** nodeArray) //returns the number of the nodes in a given node array. It ignores empty cells
{
    if(nodeArray == NULL) return 0;
    if(nodeArray[0] == 0) return 0;
    int size = 0;
    while(nodeArray[size] != 0 && nodeArray[0] != 0)
    {
        size++;
    }
    return size;
}

void freeNodeArray(int array_size, Node** nodeArray) //Nodes are allocated in memory so this funciton will free up every node in an Array, it ignores any empty cells
{
    if(array_size == 0 || nodeArray == NULL)
    {
        printf("array_size is zero\n");
        return;
    } 

    int i;
    for(i = 0; i<array_size; i++)
    {
        
        if(nodeArray[i] != 0)
        {
            free(nodeArray[i]->node_ID);
            if(nodeArray[i]->action!=NULL) free(nodeArray[i]->action);
        } 
        free(nodeArray[i]);
    }
    i = 0;
    return;
}

void incrementFringeSize(int* fringe_size, Node*** Fringe) //The size of the fringe and close is defined by a constant ARRAY_SIZE. In the case of pushing a node into full list, this function returns a larger node array with the same memory from the original
{
    int new_size = *fringe_size+1;
    Node** expandedByOne = calloc(new_size,sizeof(Node*));
    memcpy(expandedByOne, *Fringe, (*fringe_size)*sizeof(Node*));
    
    Node** tmp = *Fringe;
    *Fringe = expandedByOne;

    free(tmp);

    *fringe_size = new_size;
    return;
}

Node* makeNode(char* childName, Problem* problem) //makes a node based on a given name
{
    if(problem->informed == true) //We are doing heuristics
    {
        if(strcmp(childName,"END")==0 || strcmp(childName,"OF")==0 || strcmp(childName,"INPUT")==0)
        {
            printf("\ninside makeNode: END OF INPUT read, returning NULL\n");
            return NULL;
        } 
        else
        {
            Node* node = malloc(sizeof(Node));
            node->parent = NULL;
            node->heuristic = searchHeuristic(childName,problem);
            node->child = NULL;
            node->node_ID = childName;
            node->action = NULL;
            // node->action = action;
            node->cost = 0.0;
            return node;
        } 
    }
    else //We aren't doing heuristics
    {
        if(strcmp(childName,"END")==0 || strcmp(childName,"OF")==0 || strcmp(childName,"INPUT")==0)
        {
            printf("\ninside makeNode: END OF INPUT read, returning NULL\n");
            return NULL;
        } 
        else
        {
            Node* node = malloc(sizeof(Node));
            node->parent = NULL;
            node->heuristic = 0.0;
            node->child = NULL;
            node->node_ID = childName;
            node->action = NULL;
            // node->action = action;
            node->cost = 0.0;
            return node;
        } 
    }
}

Node* makeInitNode(Problem* problem) //makes the initial node of an empty fringe. Uses the orgin_city name
{
    if(problem-> informed == false) // we aren't doing heuristics
    {
        Node* node = calloc(1,sizeof(Node));
        node->parent = NULL;
        char* node_ID = calloc(strlen(problem->origin_city) + 1, sizeof(char));
        strcpy(node_ID,problem->origin_city);
        node->node_ID = node_ID;
        node->heuristic = 0.0;
        node->cost = 0.0;
        node->action = NULL;
        node->child = NULL;
        return node;
    }
    else // we are doing heuristics
    {
        Node* node = calloc(1,sizeof(Node));
        node->parent = NULL;
        char* node_ID = calloc(strlen(problem->origin_city) + 1, sizeof(char));
        strcpy(node_ID,problem->origin_city);
        node->node_ID = node_ID;
        node->heuristic = searchHeuristic(problem->origin_city, problem);
        node->cost = 0.0;
        node->action = NULL;
        node->child = NULL;
        return node;
    }

}

void insertSortFringe(Node** fringe, Problem* problem) //My chosen sorting alorithm. It's a stable sorting algorithm so the case that it runs into two nodes with the same key value, it will preserve relative insert order
{
    if(problem->informed == true) //we are doing heuristics
    {
        if(fringe == NULL) return;
        int size = howManyNodes(fringe);
        int i,j; float key; Node* kp;
        for(i = 1; i<size; i++)
        {
            key = (fringe[i]->cost+fringe[i]->heuristic);
            kp = fringe[i];
            j = i - 1;
            while(j>=0 && (fringe[j]->cost+fringe[j]->heuristic) > key)
            {
                fringe[j + 1] =  fringe[j];
                j = j -1;
            }
            fringe[j + 1] = kp;
        }
        return;
    }
    else //we aren't doing heuristics
    {
        if(fringe == NULL) return;
        int size = howManyNodes(fringe);
        int i,j; float key; Node* kp;
        for(i = 1; i<size; i++)
        {
            key = fringe[i]->cost;
            kp = fringe[i];
            j = i - 1;
            while(j>=0 && fringe[j]->cost > key)
            {
                fringe[j + 1] =  fringe[j];
                j = j -1;
            }
            fringe[j + 1] = kp;
        }
        return;
    }

}

bool searchClosed(Node** closed, int closed_size, Node* node ) //checks if a node is in a closed list
{
    int i;
    for(i = 0; i<closed_size; i++)
    {
        if(closed[i]!=0)
        {
            if(strcmp(closed[i]->node_ID, node->node_ID) == 0)
            {
                return true;
            }
        }

    }
    i = 0;
    return false;
}

void push(int* fringe_size, Node* node, Node*** fringe) //pushes nodes to the back of a fringe
{
    int insertIndex = howManyNodes(*fringe);
    if(insertIndex + 1 < *fringe_size)
    {
        (*fringe)[insertIndex] = node;
    }
    else
    {
        incrementFringeSize(fringe_size, fringe);
        (*fringe)[insertIndex] = node;
    }
    return;
}

Node* pop(Node*** fringe) //pops the front node in the fringe
{
    int numOfNodes = howManyNodes(*fringe);
    Node* first = *fringe[0];
    int i;
    for(i = 0; i<numOfNodes; i++)
    {
        (*fringe)[i] = (*fringe)[i+1];
    }
    i = 0;
    return first;
}

Node** successorFn(Problem* problem, Node* node) //returns an array of nodes that are succesors to the input node
{
    //calloc that successors array and look for the succesors in the file
    int successors_size = ARRAY_SIZE;
    Node** successors = calloc(successors_size, sizeof(Node));
    
    char buffer[MAX_LINE_LENGTH];
    memset(buffer,'\0',sizeof(buffer));
    
    char* token = NULL;
    char* lineArgs[3] = {};

    //this first loop creates each child and adds it to the children array
    while(fgets(buffer, sizeof(buffer),problem->ip) != NULL)
    {
        token = strtok(buffer," "); //gets the first element from each line in the file
        lineArgs[0] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[0],token);

        token = strtok(NULL," "); //gets the second element from each line in the file
        lineArgs[1] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[1],token);

        token = strtok(NULL," "); //gets the third element from each line in the file
        lineArgs[2] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[2],token);

        token = NULL;

        //at this point lineArgs contains the two cities and the cost between them
        if((strcmp(lineArgs[0],node->node_ID) == 0 || strcmp(lineArgs[1],node->node_ID) == 0 ) && (strcmp(lineArgs[0],"END")!=0 || strcmp(lineArgs[0],"OF")!=0 || strcmp(lineArgs[0],"INPUT")!=0))
        {
            Node*  childNode = NULL;
            if(strcmp(lineArgs[0],node->node_ID) == 0) //the child is in lineArgs[1]
            {
                //get the name of the child and make a node
                
                char* child_ID = calloc(strlen(lineArgs[1])+1,sizeof(char));
                strcpy(child_ID,lineArgs[1]);

                childNode = makeNode(child_ID, problem);

                free(lineArgs[0]);
                free(lineArgs[1]);
                free(lineArgs[2]);
                child_ID = NULL;
            }
            else //the child is in lineArgs[0]
            {
                //same logic as above
                char* child_ID = calloc(strlen(lineArgs[0])+1,sizeof(char));
                strcpy(child_ID,lineArgs[0]);

                childNode = makeNode(child_ID, problem);

                free(lineArgs[0]);
                free(lineArgs[1]);
                free(lineArgs[2]);
                child_ID = NULL;
            }
            childNode->parent = node;
            push(&successors_size, childNode, &successors);
        }
        else
        {
            free(lineArgs[0]); free(lineArgs[1]); free(lineArgs[2]);
        } 
        lineArgs[0] = NULL;
        lineArgs[1] = NULL;
        lineArgs[2] = NULL;
        memset(buffer,'\0',sizeof(buffer));
    }
    lineArgs[0] = NULL;
    lineArgs[1] = NULL;
    lineArgs[2] = NULL;
    rewind(problem->ip);
    return successors;
}

float stepCost(Node* node, Node* s, Problem* problem) // returns the weight of an edge betweeen two adjacent nodes
{
    float stepcost = 0.0;
    char buffer[MAX_LINE_LENGTH];
    memset(buffer,'\0',sizeof(buffer));
    
    char* token = NULL;
    char* lineArgs[3] = {};
    while(fgets(buffer, sizeof(buffer),problem->ip) != NULL)
    {
        token = strtok(buffer," "); //gets the first element from each line in the file
        lineArgs[0] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[0],token);

        token = strtok(NULL," "); //gets the second element from each line in the file
        lineArgs[1] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[1],token);

        token = strtok(NULL," "); //gets the third element from each line in the file
        lineArgs[2] = calloc(strlen(token)+1,sizeof(char));
        strcpy(lineArgs[2],token);
        
        token = NULL;

        if((strcmp(lineArgs[0],node->node_ID) == 0 && strcmp(lineArgs[1],s->node_ID) == 0 ) || 
        (strcmp(lineArgs[1],node->node_ID) == 0 && strcmp(lineArgs[0],s->node_ID) == 0 ) && (strcmp(lineArgs[0],"END")!=0 || strcmp(lineArgs[0],"OF")!=0 || strcmp(lineArgs[0],"INPUT")!=0))
        {
            stepcost = atof(lineArgs[2]);
        }
        free(lineArgs[0]);free(lineArgs[1]);free(lineArgs[2]);
        memset(buffer,'\0',sizeof(buffer));
    }
    rewind(problem->ip);
    return stepcost;
}

Node** initFringe(int* fringe_size, Problem* problem) //allocates memory for the fringe, makes and pushes the first node
{
    // create an empty fringe
    Node** fringe = calloc(*fringe_size, sizeof(Node*));

    // we gotta find the origin city in the file

    // make a node using the origin city
    Node* root = makeInitNode(problem);

    // insert initial node into the fringe
    push(fringe_size, root, &fringe);

    // return fringe
    return fringe;
}

Node* goalTest(Problem* problem, Node* node)
{
    if(strcmp(problem->destination_city,node->node_ID) == 0) return node;
    else
        return NULL;
}

Node** expand(Problem* problem, Node* node, Result* result) // configures values for each child node that is returned from successorFn()
{
    Node** children = successorFn(problem, node);
    int children_num = howManyNodes(children);
    int successors_size = children_num + 1;
    Node** successors = calloc(successors_size, sizeof(Node));
    int i;
    for(i = 0; i<children_num; i++)
    {
        Node* s = calloc(1, sizeof(Node));
        //Assign Parent Node
        s->parent = node;
        //Assign Node ID
        s->node_ID = (children[i])->node_ID;
        //Assign Heuristic
        s->heuristic = (children[i])->heuristic;
        //Assign Action
        s->action = (children[i])->action;        
        //Assign Path Cost
        s->cost = node->cost + stepCost(node,s,problem);        
        //Assign Child Node
        s->child = (children[i])->child;

        push(&successors_size, s, &successors);
        result->nodesGenerated++;
        if(children[i] != 0) free(children[i]);
    }
    i = 0;
    free(children);
    result->nodesExpanded++;
    return successors;
}

void insertAll(Node** successors, Node*** fringe, int* fringe_size, Problem* problem) //pushes all successor nodes returned from expand() to a fringe and then sorts the fringe
{
    int succNodeNum = howManyNodes(successors);
    int successors_size = succNodeNum + 1;
    int i;
    for(i = 0; i<succNodeNum; i++)
    {
        push(fringe_size, successors[i], fringe);
    }
    i = 0;
    insertSortFringe(*fringe, problem);
    free(successors);
    return;
}

Node* graphSearch(Problem* problem, Result* result)
{
    int fringe_size = ARRAY_SIZE;
    int closed_size = ARRAY_SIZE;
    Node** closed = calloc(closed_size, sizeof(Node*));
    Node** fringe = initFringe(&fringe_size, problem);
    result->nodesGenerated++;

    while(1==1)
    {
        if(fringe[0] == 0) //fringe is empty
        {
            result->infinite = true;       
            result->fringe = fringe;       
            result->fringe_size = fringe_size;       
            result->closed = closed;       
            result->closed_size = closed_size;
            return NULL;
        }
        Node* node = pop(&fringe);
        result->nodesPoped++;
        
        if(goalTest(problem,node) != NULL) //found destination
        {   
            result->infinite = false;       
            result->fringe = fringe;       
            result->fringe_size = fringe_size;       
            result->closed = closed;       
            result->closed_size = closed_size;
            result->distance = node->cost;       
            return node;
        } 
        //search if the node is in closed
        if(searchClosed(closed,closed_size,node) == false)
        {
            push(&closed_size, node, &closed);
            insertAll(expand(problem,node,result),&fringe,&fringe_size, problem); //expand node
        } 
        else
        {
            if(node->action != NULL) free(node->action);
            free(node->node_ID);
            free(node);
        } 
    }
}

void printRoute(Node* node, Problem* problem) //So far all nodes only point to their parents, this function will configure the correct children pointers and then prints the optimal path
{
    Node* current = NULL;
    Node* next = NULL;
    current = node;
    next = node->parent;
    //We start from the end of the link list (e.i. the destination node)
    while(next!=NULL) //configuring children nodes
    {
        next->child = current;
        current = next;
        next = current->parent;
    }
    //We finished traversing backwards in the link list
    //Now to print out the linked list of nodes starting from the origin city node
    next = current->child;
    printf("Route:\n");
    while(current != NULL && next != NULL)
    {
        if(current != NULL)
        {
            printNodeID(current->node_ID); printf(" to "); printNodeID(next->node_ID); printf(", %.1f km\n",stepCost(current,next,problem));
        }
        current = next;
        if(current != NULL) next = current->child;
    }
}