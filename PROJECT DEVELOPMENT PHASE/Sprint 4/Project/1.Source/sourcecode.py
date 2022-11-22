DetailsTrack.jsx 
import React from 'react'; import { Line } from 'react-chartjs-2'; import useTransactions from '../../useTransactions'; import './detailsTrack.css'; 
 
const DetailsTrack = ({ title }) => { 
 
    const { chartDataIncome, chartDataExpense } = useTransactions(title); 
 
    const chartData = (title === 'Income') ? chartDataIncome : chartDataExpense; 
 
    return ( 
        <div className='chartContainer'> 
            <div className={title === 'Income' ? 'incomeChart' : 'expenseChart'} > 
                <Line data={chartData} /> 
            </div> 
        </div> 
    ); 
}; 
 
export default DetailsTrack; 
 
detailsTrack.css 
.incomeChart {     background-color: white;     border: 5px solid rgb(147, 147, 147);     margin: 20px 200px;     padding: 50px;     border-radius: 10px; 
} 
 
.expenseChart {     background-color: white;     border: 5px solid rgb(147, 147, 147);     margin: 20px 200px;     padding: 50px;     border-radius: 10px; 
     
} 
 
Snackbar.jsx 
import React from 'react' import Snackbar from '@mui/material/Snackbar'; import MuiAlert from '@mui/material/Alert'; 
 
 
const CustomizedSnackbar = ({ title, open, setOpen }) => { 
 
 
    const handleClose = (event, reason) => {         if (reason === 'clickaway') return;         setOpen(false); 
    } 
 
    return ( 
        <div> 
            {title === 'list' && 
                <div className='root'> 
                    <Snackbar                         anchorOrigin={{ vertical: 'top', horizontal: 'right' }}                         open={open}                         autoHideDuration={3000}                         onClose={handleClose} 
                    > 
                        <MuiAlert onClose={handleClose} severity="success" elevation={6} variant="filled" > 
                            Category successfully Removed 
                        </MuiAlert> 
                    </Snackbar> 
                </div> 
            } 
            {title === 'form' && 
                <div className='root'> 
                    <Snackbar                         anchorOrigin={{ vertical: 'top', horizontal: 'right' }}                         open={open}                         autoHideDuration={3000}                         onClose={handleClose} 
                    > 
                        <MuiAlert onClose={handleClose} severity="success" elevation={6} variant="filled" > 
                            Category successfully Added 
                        </MuiAlert> 
                    </Snackbar> 
                </div> 
            } 
            {title === 'unfilled' && 
                <div className='root'> 
                    <Snackbar                         anchorOrigin={{ vertical: 'top', horizontal: 'right' }}                         open={open}                         autoHideDuration={3000}                         onClose={handleClose} 
                    > 
                        <MuiAlert onClose={handleClose} severity="warning" elevation={6} variant="filled" > 
                            Unfulfilled fields..!! 
                        </MuiAlert> 
                    </Snackbar> 
                </div> 
            } 
             
        </div> 
         
    ); 
}; 
 
export default CustomizedSnackbar; 
 
SnackbarStyles.js 
import { makeStyles } from '@material-ui/core/styles'; 
 
export default makeStyles((theme) => ({ 
  root: {     width: '100%',     '& > * + *': {       marginTop: theme.spacing(2), 
    }, 
  }, 
})); 
 
snackbar.css 
.root {     width: 100%;  
} 
 
categories.js 
const incomeColors = ['#123123', '#154731', '#165f40', '#16784f', '#14915f', '#10ac6e', 
'#0bc77e', '#04e38d', '#00ff9d']; 
const expenseColors = ['#b50d12', '#bf2f1f', '#c9452c', '#d3583a', '#dc6a48', '#e57c58', '#ee8d68', '#f79d79', '#ffae8a', '#cc474b', '#f55b5f']; 
 
export const incomeCategories = [ 
  { type: 'Business', amount: 0, color: incomeColors[0] }, 
  { type: 'Investments', amount: 0, color: incomeColors[1] }, 
  { type: 'Extra income', amount: 0, color: incomeColors[2] }, 
  { type: 'Deposits', amount: 0, color: incomeColors[3] }, 
  { type: 'Lottery', amount: 0, color: incomeColors[4] }, 
  { type: 'Gifts', amount: 0, color: incomeColors[5] }, 
  { type: 'Salary', amount: 0, color: incomeColors[6] }, 
  { type: 'Savings', amount: 0, color: incomeColors[7] }, 
  { type: 'Rental income', amount: 0, color: incomeColors[8] }, 
]; 
 
export const expenseCategories = [ 
  { type: 'Bills', amount: 0, color: expenseColors[0] }, 
  { type: 'Car', amount: 0, color: expenseColors[1] }, 
  { type: 'Clothes', amount: 0, color: expenseColors[2] }, 
  { type: 'Travel', amount: 0, color: expenseColors[3] }, 
  { type: 'Food', amount: 0, color: expenseColors[4] }, 
  { type: 'Shopping', amount: 0, color: expenseColors[5] }, 
  { type: 'House', amount: 0, color: expenseColors[6] }, 
  { type: 'Entertainment', amount: 0, color: expenseColors[7] }, 
  { type: 'Phone', amount: 0, color: expenseColors[8] }, 
  { type: 'Pets', amount: 0, color: expenseColors[9] }, 
  { type: 'Other', amount: 0, color: expenseColors[10] }, 
]; 
 
export const resetCategories = () => {   incomeCategories.forEach((c) => c.amount = 0);   expenseCategories.forEach((c) => c.amount = 0); 
}; 
 
formatDate.js 
const formatDate = (date) => {     const d = new Date(date); 
 
    let month = `${d.getMonth() + 1}`;     let day = `${d.getDate()}`;     const year = d.getFullYear(); 
 
    if (month.length < 2) {         month = `0${month}`; 
    } 
    if (day.length < 2) {         day = `0${day}`; 
    } 
 
    return [year, month, day].join('-'); 
} 
 
export default formatDate; 
 
main.py 
import flask from flask import Flask, render_template  import ibm_db 
 
 
app = Flask("__main__") 
 
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY= SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hln67748;PWD=yRDx30Fb0x6 kA8Db",'','') 
 
 
@app.route("/") 
 
def my_index(): 
    return flask.render_template("index.html", token="Hello World") 
 
app.run(debug=True) 
 
