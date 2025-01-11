#include<bits/stdc++.h>
#include <random>
#include <ctime>
#include <fstream> 
using namespace std;
const int INF=1e9;
vector<int>xc,yc,zc;
int n;
int p;
int globaltotal;
int t0;

vector<vector<vector<int>>>globalpath;
vector<vector<vector<int>>>points;
vector<int>globalcost;
vector<int>globalorder;
pair<int,vector<vector<int>>>dijk(vector<int>s,vector<int>e,vector<vector<vector<int>>>grid){

    vector<vector<vector<int>>> dis(n + 1, vector<vector<int>>(n + 1, vector<int>(n + 1, INF)));
    vector<vector<vector<vector<int>>>>par(n+1,vector<vector<vector<int>>>(n+1,vector<vector<int>>(n+1)));
    priority_queue<pair<int,vector<int>>,vector<pair<int,vector<int>>>,greater<pair<int,vector<int>>>>q;
    dis[s[0]][s[1]][s[2]]=grid[s[0]][s[1]][s[2]];
    q.push({grid[s[0]][s[1]][s[2]],s});

    while(q.empty()!=true){

        int distance=q.top().first;
        vector<int> node=q.top().second;
        q.pop();

       if(distance>dis[node[0]][node[1]][node[2]]) continue;

        for(int i=0;i<6;i++){
            int newx=node[0]+xc[i];
            int newy=node[1]+yc[i];
            int newz=node[2]+zc[i];

            if(newx>=0 && newx<=n && newy>=0 && newy<=n && newz>=0 && newz<=n){
                vector<int>newnode={newx,newy,newz};
                
                int newdis=distance+grid[newx][newy][newz];

                if(dis[newx][newy][newz]>newdis){
                    dis[newx][newy][newz]=newdis;
                    q.push({newdis,newnode});
                    par[newx][newy][newz]=node;
                }
            }
        }
    }


    int cost=dis[e[0]][e[1]][e[2]];
    vector<vector<int>>path;
    vector<int>node=e;

    if(cost!=INF){
        while(node!=s){
            path.push_back(node);
            node=par[node[0]][node[1]][node[2]];
        }
        path.push_back(s);
        reverse(path.begin(),path.end());
    }
    return {cost,path};
}

void rec(int bitmask,vector<int>order,vector<vector<vector<int>>>path,vector<int>cost,int total,vector<vector<vector<int>>>grid){
    if(bitmask==((1<<p)-1)){
        if(total<globaltotal){
            globaltotal=total;
            globalpath=path;
            globalcost=cost;
            globalorder=order;
        
        }
        
        return;
    }
    for(int i=0;i<p;i++){
        if((bitmask&(1<<i))==0){
            pair<int,vector<vector<int>>>temp=dijk(points[i][0],points[i][1],grid);

            if(temp.first<INF){
                vector<vector<int>>temppath=temp.second;
                vector<vector<vector<int>>>newgrid=grid;
                for(int j=0;j<temppath.size();j++){
                    newgrid[temppath[j][0]][temppath[j][1]][temppath[j][2]]=INF;
                }
                order.push_back(i);
                path.push_back(temppath);
                cost.push_back(temp.first);
                rec((bitmask|(1<<i)),order,path,cost,temp.first+total,newgrid);
                path.pop_back();
                cost.pop_back();
                order.pop_back();
                
            }
        }
    }
    return;
}
int main(){

    ofstream outFile;
    outFile.open("output.txt");

    ofstream totalpaths;
    totalpaths.open("paths.txt");

    ofstream totalpoints;
    totalpoints.open("points.txt");

    random_device rd;
    mt19937 gen(rd() ^ time(0));
    uniform_int_distribution<> dist(2, 100);

    xc={1,-1,0,0,0,0};
    yc={0,0,1,-1,0,0};
    zc={0,0,0,0,1,-1};

    

    n=10;
    t0=1;

    vector<vector<vector<int>>>grid(n+1,vector<vector<int>>(n+1,vector<int>(n+1,t0)));
    for(int i=0;i<n+1;i++){
        for(int j=0;j<n+1;j++){
            for(int k=0;k<n+1;k++){
                    int r_no=dist(gen);
                    if(r_no>50){

                    int new_random=dist(gen);
                    grid[i][j][k]+=new_random;

                    }
                    
                
            }
        }
    }
    for(int i=0;i<=n;i++){
        for(int j=0;j<=n;j++){
            for(int k=0;k<=n;k++){
                outFile<<i<<" "<<j<<" "<<k<<" "<<grid[i][j][k]<<endl;
            }
        }
    }
    p=4;
    vector<int>order;
    globalorder.clear();
    vector<vector<vector<int>>>path;
    globalpath.clear();
    vector<int>cost;
    globalcost.clear();
    
    int total=0;
    globaltotal=INF;
    int bitmask=0;
    points.clear();
    points={{{9,4,1},{3,3,8}},{{0,0,0},{1,1,1}},{{2,2,2},{3,7,2}},{{1,9,2},{1,3,4}}};

    for(int j=0;j<p;j++){
        totalpoints<<points[j][0][0]<<" "<<points[j][0][1]<<" "<<points[j][0][2]<<endl;
        totalpoints<<points[j][1][0]<<" "<<points[j][1][1]<<" "<<points[j][1][2]<<endl;
        totalpoints<<endl;
    }
    
    rec(bitmask,order,path,cost,total,grid);

    totalpaths<<globaltotal<<endl;
    for(int i=0;i<globalorder.size();i++){
        totalpaths<<globalorder[i]<<" ";
    }
    totalpaths<<endl;
    for(int j=0;j<globalpath.size();j++){
        totalpaths<<globalcost[j]<<endl;
        for(int i=0;i<globalpath[j].size();i++){
            totalpaths<<globalpath[j][i][0]<<" "<<globalpath[j][i][1]<<" "<<globalpath[j][i][2]<<endl;
        }
        totalpaths<<endl;
    }
    

}