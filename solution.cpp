#include <bits/stdc++.h>

using namespace std;

int main() {
#ifdef _DEBUG
	freopen("input.txt", "r", stdin);
//	freopen("output.txt", "w", stdout);
#endif
	
	int t, i, j;
	long long int n, m, x;
	cin >> t;
	while (t--) {
		cin>>n>>m>>x;
		i = x/m;
		if (x%m != 0){
			i++;
		}
		j = x/n;
		if (x%n != 0){
			j++;
		}

		cout<<((i-1)*m)+j<<endl;

	}
	
	return 0;
}