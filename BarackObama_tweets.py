#pip install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
import twint as tw
import nest_asyncio
import pandas as pd

def main():
    nest_asyncio.apply()
    a = tw.Config()
    a.Username = 'BarackObama'
    a.Profile=True
    a.Since = "2020-1-01"
    a.Store_csv = True
    a.Output = a.Username + ".csv"
    a.Search = "covid 19"
    all_tw=tw.run.Search(a)
    return all_tw


if __name__ == '__main__':
    all_tw=main()

df_all_tw = pd.read_csv("BarackObama.csv")
df_all_tw=df_all_tw[['id','date','name','tweet']]

print(df_all_tw)
df_all_tw.to_csv("BarackObama.csv", index=False)

