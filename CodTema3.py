# ===============================
# 0. OPRIRE WARNINGURI
# ===============================
import warnings
warnings.filterwarnings("ignore")

# ===============================
# 1. IMPORTURI
# ===============================
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori, association_rules

# ===============================
# 2. ÎNCĂRCARE DATE (ITALIA)
# ===============================
df = pd.read_csv(
    '/content/consumption_user.csv',   # ← fișierul ITALIA
    encoding='latin1',
    low_memory=False
)

# ===============================
# 3. COLOANE CORECTE (FAO – SIGUR)
# ===============================
cols = {c.lower(): c for c in df.columns}

id_col   = next(v for k, v in cols.items() if "subj" in k or "id" in k)
day_col  = next(v for k, v in cols.items() if "day" in k)
food_col = next(v for k, v in cols.items() if "food" in k or "foode" in k)

df = df[[id_col, day_col, food_col]]
df.columns = ["id", "day", "food"]

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
# ===============================
# 4. TRANZACȚII (CORECTE)
# ===============================
df["tx"] = df["id"].astype(str) + "_" + df["day"].astype(str)

transactions = (
    df.groupby("tx")["food"]
      .apply(lambda x: list(set(x)))
)

# eliminăm tranzacții cu 1 singur aliment (FOARTE IMPORTANT)
transactions = transactions[transactions.apply(len) > 1]

# limitare anti-blocare
transactions = transactions.sample(
    n=min(6000, len(transactions)),
    random_state=42
)
# ===============================
# 5. ENCODARE
# ===============================
te = TransactionEncoder()
X = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(X, columns=te.columns_)

# FP-GROWTH – PARAMETRI SIGURI
freq_fp = fpgrowth(
    df_encoded,
    min_support=0.1,   # MARE => RAPID
    use_colnames=True,
    max_len=2
)
# ===============================
# 7. APRIORI (COMPARAȚIE)
# ===============================
freq_ap = apriori(
    df_encoded,
    min_support=0.02,
    use_colnames=True,
    max_len=2
)

print("Apriori itemsets:", len(freq_ap))
Apriori itemsets: 2235
________________________________________
# ===============================
# 8. STATISTICI DESCRIPTIVE
# ===============================
print("Număr observații:", df.shape[0])
print("Număr tranzacții:", len(transactions))
print("Număr alimente distincte:", df['food'].nunique())

df['food'].value_counts().head(10)
Număr observații: 212370
Număr tranzacții: 6000
Număr alimente distincte: 878

# ===============================
# 9. SALVARE REZULTATE
# ===============================
freq_fp.to_csv('fp_itemsets.csv', index=False)
rules_fp.to_csv('fp_rules.csv', index=False)
freq_ap.to_csv('apriori_itemsets.csv', index=False)

