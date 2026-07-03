import io
import os
import base64
from flask import Flask, render_template, request, send_file, url_for, session, redirect
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from Registration import auth, bcrypt



app = Flask(__name__)

app.secret_key = "your-secret-key"
bcrypt.init_app(app)
app.register_blueprint(auth)


df = None
duplicates_table = None
describe_table = None
info_table = None
head_table = None
tail_table = None
graph_url = None


def get_connector():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Varun@2003",
        database = "cleanmydata"
    )

def save_action(action_name, file_name):
    conn = get_connector()
    cursor = conn.cursor()
    rows = len(df)
    cols = len(df.columns)
    cursor.execute(
        "INSERT INTO uploaded_files (action_name, file_name, total_rows, total_columns)VALUES(%s,%s,%s,%s)",
        (action_name, file_name, rows, cols)
    )
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=["GET","POST"])
def fill_data():

    if "user" not in session:
        return redirect(url_for("auth.login"))
        
    global df, master_table, duplicates_table, describe_table, info_table ,head_table, tail_table
    errors = None
    master_table = None


    if request.method == "POST":
        # 1. Uploading the Data file resets the master table
        file = request.files.get("File")
        if file and file.filename != "":
            df = pd.read_csv(file)
            save_action("File Uploded" ,file.filename)




    if request.method == "POST" and df is not None:


        duplicated = request.form.get("duplicat_ed")
        head = request.form.get("head")
        tail = request.form.get("tail")
        if df is not None and duplicated and duplicated in df.columns:
            
            #df = df.drop_duplicates(duplicated)
            duplicatestable = df[df.duplicated(duplicated)]
            duplicates_table = duplicatestable.to_html(classes="table")
            save_action("Duplicated" ,duplicated)

            describetable = df.describe()
            describe_table = describetable.to_html(classes="table")


            infotable = pd.DataFrame(
            {
                "Column":df.columns,
                "Non-Null Count":df.notnull().sum().values,
                "Dtype":df.dtypes.values,
            }
            )
            info_table = infotable.to_html(classes="table", index=False)


            head = pd.to_numeric(head)
            headtable = df.head(head)
            head_table = headtable.to_html(classes="table")

            tail = pd.to_numeric(tail)
            tailtable = df.tail(tail)
            tail_table = tailtable.to_html(classes="table")

            return render_template("index1.html",duplicates_table=duplicates_table, describe_table=describe_table, info_table=info_table ,head_table=head_table, tail_table=tail_table, username=session["user"])


        fill1 = request.form.get("Full_Columns")
        Custom_Value1 = request.form.get("Custom_Value")

        if df is not None and fill1 :

            if fill1 not in df.columns:
                errors = f"Column '{fill1}' not found. "
            else:
                df[fill1] = df[fill1].fillna(Custom_Value1)
                save_action(" Fill with Custom Value" ,fill1)




        
        fill2 = request.form.get("Fill_with_mean")
        if df is not None and fill2:

            if fill2 not in df.columns:
                errors = f"Column '{fill2}' not found."

            elif not pd.api.types.is_numeric_dtype(df[fill2]):
                errors = f"Column '{fill2}' is not numeric."

            else:
                means = df[fill2].mean()
                df[fill2] = df[fill2].fillna(means)
                save_action("Fill with Mean" ,fill2)



        


        fill3 = request.form.get("Fill_Numbers")
        custom_num2 = request.form.get("Custom_Num_Value")
        if df is not None and fill3:
            if fill3 not in df.columns:
                errors = f"Column '{fill3}' not found."

            elif not pd.api.types.is_numeric_dtype(df[fill3]):
                errors = f"Column '{fill3}' is not numeric."
            else:
                df[fill3] = df[fill3].fillna(custom_num2)
                save_action("Fill Specific Number" ,fill3)





        drop = request.form.get("Drop")
        if df is not None and drop:
            if drop not in df.columns:
                errors = f"Column '{drop}' not found."
            else:
                df = df.dropna(subset=[drop])
                save_action("Fill Specific Number" ,fill3)




        drop1 = request.form.get("Drop_col")
        if df is not None and drop1 :
            if drop1 not in df.columns:
                errors = f" Column '{drop1}' not found."
            else:
                df = df.drop(columns=[drop1])
                save_action("Drop Entire Column" ,drop1)

            



        To_Numaric = request.form.get("tonumaric")
        if df is not None and To_Numaric :
            if To_Numaric not in df.columns:
                errors = f"Column '{To_Numaric}' not found."
  
            else:
                df[To_Numaric] = pd.to_numeric(df[To_Numaric], errors="coerce")
                save_action("Convert Type to Numeric" ,To_Numaric)
            


        To_Date = request.form.get("DateTime")
        if df is not None and To_Date and To_Date in df.columns:
            if To_Date not in df.columns:
                errors = f"Column '{To_Date}' not found."

            else:
                df[To_Date] = pd.to_datetime(df[To_Date], errors="coerce")
                save_action("Convert Type to DateTime" ,To_Date)




        Unique = request.form.get("UniqueValues")
        if df is not None and Unique:
            if Unique not in df.columns:
                errors = f"Column '{Unique}' not found."
            
            else:
                unique_value = df[Unique].unique()
                Unique_Val = pd.DataFrame(unique_value, columns=["Unique Values"])
                master_table = Unique_Val.to_html(classes="table", index=False)
                save_action("Check Unique Values" ,Unique)
                return render_template("index.html", master_table=master_table, errors=errors,username=session["user"])





        CountUnique = request.form.get("Count_Unique_Val")
        if df is not None and CountUnique:
            if CountUnique not in df.columns:
                errors = f"Column '{CountUnique}' not found."
            
            else:
                Counts_DF  = df[CountUnique].value_counts().to_frame(name="Total value")
                master_table = Counts_DF.to_html(classes="table")
                save_action("Count Unique Values" ,CountUnique)
                return render_template("index.html", master_table=master_table, errors=errors, username=session["user"])



        # Rename Columns
        RenameColumns = request.form.get("Rename_Column")
        NewColumn = request.form.get("New_Column")
        if df is not None and RenameColumns:
            
            if RenameColumns not in df.columns:
                errors = f"Column '{RenameColumns}' not found."
            
            else:
                df = df.rename(columns={RenameColumns:NewColumn})
                save_action("Rename Columns" ,RenameColumns)


            


        FilterData = request.form.get("Filters_Data1")
        InputNumber = request.form.get("InputNumber")
        Operator_Choice = request.form.get("Operator_Choice")
        if df is not None and FilterData :

            if FilterData not in df.columns:
                errors = f"Column '{FilterData}' not found."
            else:
                temp_df = df.copy()
            
                try:
                    Input_Number = float(InputNumber) 
                    temp_df[FilterData] = pd.to_numeric(temp_df[FilterData], errors="coerce")

                    # df = df[df[FilterData] , Operator_Choice, Input_Number]

                    if Operator_Choice == "<":
                        filtered_df = temp_df[temp_df[FilterData] < Input_Number]
                    elif Operator_Choice == ">":
                        filtered_df = temp_df[temp_df[FilterData] > Input_Number]
                    elif Operator_Choice == "==":
                        filtered_df = temp_df[temp_df[FilterData] == Input_Number]

                    
                        
                        

                except ValueError:
                    if FilterData not in df.columns:
                        errors = f"Column '{FilterData}' not found."

                    else:
                        filtered_df = temp_df[temp_df[FilterData] == InputNumber]

                master_table = filtered_df.to_html(classes="table")
                return render_template("index.html", master_table=master_table, errors=errors)            
        


    updated_table = df.to_html(classes='table') if df is not None else None 
    return render_template("index.html" , master_table=updated_table, errors=errors, username=session["user"])




@app.route('/Plot' , methods=['POST'])
def Plots():

    errors = None  

    global graph_url, df

    first = request.form.get("First")
    second = request.form.get("Second", "").strip() or None
    Options1 = request.form.get("Options1")
    Filename = request.form.get("Filename")
    Tital = request.form.get("Tital")

            
    if (first and first not in df.columns) or second not in df.columns:
        errors = f"Column '{first}' or '{second}' not found."

    if df is None:
        errors = f"No dataset found. Please upload a file first."
        return render_template("plots.html", errors=errors, graph_url=None)


    required_both = ["bar", "line", "area", "pie", "scatter","CountPlot","heatmap"]
    if Options1 in required_both and (not first or not second):
        errors = f"Both 'First' and 'Second' column selections are compulsory for a ' {Options1.capitalize()} ' plot."
        return render_template("plots.html", errors=errors, graph_url=None)


    if Options1 in ["boxplot","hist"] and not second:
        errors = f"Using '{Options1.capitalize()} Plot', please fill out the 'Second' input section."
        return render_template("plots.html", errors=errors, graph_url=None)
        
                    
    elif df[[first,second]].isnull().any().any() if first else df[second].isnull().any():
        errors = f"Put the valid values in '{first}' or '{second}' selected columns."
                                    
    elif Options1 in ["bar", "line", "area", "pie", "hist", "scatter", "boxplot","heatmap","CountPlot"] :

        plt.clf()

        
        if Options1 == "scatter":
            if not pd.api.types.is_numeric_dtype(df[first]) and pd.api.types.is_numeric_dtype(df[second]):
                errors = f"Using 'Scatter Plot' Fill only Numeric vlues column in both input section "
            else:
                plt.scatter(df[first], df[second])



        elif Options1 == "boxplot":

            if not pd.api.types.is_numeric_dtype(df[second]):
                errors = f"Using 'Box Plot' Fill only Numeric vlues column in input section " 
            else:
                if first:
                    errors = f"Don't need to write ' first ' input onlly write ' Second ' input section"
                else:
                    plt.boxplot(df[second]) 



        elif Options1 == "hist" :
            if not pd.api.types.is_numeric_dtype(df[second]):
                errors = f"Using 'Histogram' Fill only Numeric vlues column in input section "
            else:
                if first:
                    errors = f"Don't need to write ' first ' input onlly write ' Second ' input section"
                else:
                    df[second].plot(kind="hist")



        elif Options1 == "CountPlot" :
            df.groupby(first)[second].value_counts().plot(kind="bar")



        elif Options1 == "heatmap":
            if not pd.api.types.is_numeric_dtype(df[first]) and pd.api.types.is_numeric_dtype(df[second]):
                errors = f"Using 'Heatmap' Fill only Numeric vlues column in both input section "

            else:
                sns.heatmap(df.corr(numeric_only=True), annot=True)




        elif Options1 in ["bar", "line", "area", "pie"] and first and pd.api.types.is_numeric_dtype(df[second]):
            plot_kwargs = {"kind": Options1}
            if Options1 == "pie":
                plot_kwargs["autopct"] = "%1.1f%%"
            df.groupby(first)[second].sum().plot(**plot_kwargs)




        plt.title(Tital)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format="png")
        # filename = f"{Filename}.png"
        # img = os.path.join("static", filename)
        
        img.seek(0)
        
    

        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        graph_url = f"data:image/png;base64,{plot_url}"
        #  f"data:image/png"
        plt.close()

                    
                    
    return render_template("plots.html", errors=errors, graph_url=graph_url)

        





@app.route('/download', methods=['POST'])
def download_data():
    global df

    if df is not None:
        custom_name = request.form.get("filename_input", "cleaned_data")

        if not custom_name.strip():
            custom_name = "cleaned_data"

        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype = "text/csv",
            as_attachment=True,
            download_name=custom_name,
        )

        
@app.route('/logs')
def logs():

    conn = get_connector()

    query = "SELECT * FROM uploaded_files ORDER BY id DESC"

    log_df = pd.read_sql(query, conn)

    print(log_df)   # ADD THIS

    conn.close()

    logs_list = log_df.to_dict(orient="records")

    print(logs_list)   # ADD THIS

    return render_template("logs.html",logs=logs_list)


    

@app.route('/logs/delete/<int:log_id>', methods=['POST'])
def delete_single_log(log_id):
    conn = get_connector()
    cursor = conn.cursor()
    query = """ DELETE FROM uploaded_files where id = %s """
    cursor.execute(query, (log_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('logs'))


@app.route('/logs/clear-all', methods=["POST"])
def clear_all_logs():
    conn = get_connector()
    cursor = conn.cursor()
    query = """ DELETE FROM uploaded_files """
    cursor.execute(query)
    conn.commit()
    conn.close()
    return redirect(url_for('logs'))

print(app.url_map)





if __name__ == "__main__":
    app.run(debug=True, port=5000)



