'use strict'

// var aws = require('aws-sdk')

const AWS = require('aws-sdk');
const ddb = new AWS.DynamoDB.DocumentClient({region: 'us-east-1'});

var lambda = new AWS.Lambda({
  region: 'us-east-1' 
})

exports.handler = async (event, context, callback) => {
    
    if(event.queryStringParameters){ //if it is a GET with parameters in query URL
        
        if(event.queryStringParameters.email && event.queryStringParameters.keyword){
            
            const emailAddress = event.queryStringParameters.email
            const key = event.queryStringParameters.keyword
            
            let db_read = await invokeLambdaReadDB(emailAddress)
            
            const res = {
                statusCode: 200,
                body: db_read
            }
            
            let id_when_found
            let body_when_found
            
            let alert_item_found = false
            
            if(JSON.parse(res.body).body){
                
                let b = JSON.parse(res.body).body.filter((e, i) => {
                    
                    if(e.message === key){
                        
                        alert_item_found = true
                        
                        console.log('here too')
                        
                        const found_res = {
                            statusCode: 200,
                            body: `You already asked this question. Previous response: ${e.answer}`,
                            id: e.ID
                        }
                        
                        id_when_found = found_res.id
                        body_when_found = found_res.body

                        return found_res.body
                    }

                })

                
                if(b[0] !== undefined && alert_item_found === true){ // question was asked before
                    console.log('here')
                    let previous_res_email = await sesEmail(emailAddress, "awsemailses@gmail.com", "Your Previous Question", body_when_found)
                    
                    const res_to_email = {
                        statusCode: 200,
                        body: previous_res_email,
                        id: id_when_found
                    }
                    
                    console.log('res_to_email: ' + previous_res_email)
                    
                    let bod = JSON.parse(previous_res_email).body
                    
                    return {
                        // 'statusCode': 200,
                        'body': bod,
                        'id': res_to_email.id
                    }
                }
            }
            
            let ai_res = await responseAI(key)
            
            // console.log('AI: ' + ai_res.body)
            
            const ai_res_back = {
                statusCode: 200,
                body: ai_res
            }
            
            console.log(JSON.parse(ai_res_back.body).body)
            let ai_res_back_second = JSON.parse(ai_res_back.body).body
            
            const requestId = context.awsRequestId
            
            // let writeDB = await invokeLambdaWriteDB(requestId, emailAddress, key, null, analyze_keyPhrase, analyze_sentiment)
            let writeDB = await invokeLambdaWriteDB(requestId, emailAddress, key, null, ai_res_back_second)

            const dbRes = {
                statusCode: 200,
                body: writeDB
            }
            
            console.log(dbRes)
            
            let ses_email = await sesEmail(emailAddress, "awsemailses@gmail.com", "Customer Service Response", ai_res_back_second) //to, from
            
            const email_res = {
                statusCode: 200,
                body: ses_email,
                id: requestId
            }
            
            // context.succeed("done")
            
            return {
                // statusCode: 200,
                body: ai_res_back_second, 
                id: email_res.id
            }
            
        }
        
    }
    
    else if(event.body){ // POST
        
        const rating = JSON.parse(event.body).rating
        const id = JSON.parse(event.body).id
        
        let updateDB = await invokeLambdaUpdateDB(id, parseInt(rating))
        
        const send_back = {
            statusCode: 200,
            // body: JSON.parse(event.body)
            body: updateDB,
            // id: id
        }
        
        return send_back
    }
}

const sesEmail = async (to, from, subject, text) => {
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'Email_SES',
            Payload: JSON.stringify({
                to, from, subject, text
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}

const responseAI = async (user_text) => {
    
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'ResponseAI',
            Payload: JSON.stringify({
                user_text
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}

const sentenceAnalyze = async (text) => {
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'analyze-text',
            Payload: JSON.stringify({
                text
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}

const invokeLambdaReadDB = async (inp) => {
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'DynamoNodeRead',
            Payload: JSON.stringify({
                inp
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}

const invokeLambdaWriteDB = async (requestId, email, inp, rating, answer) => {
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'DynamoNode',
            Payload: JSON.stringify({
                requestId,
                email,
                inp,
                rating,
                answer
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}

const invokeLambdaUpdateDB = async (requestId, rating) => {
    return await new Promise((resolve, reject) => {
        const params = {
            FunctionName: 'DynamoUpdate',
            Payload: JSON.stringify({
                requestId,
                rating
            })
        }
        
        lambda.invoke(params, (err, results) => {
            if(err){ 
                reject(err)
            }
            else {
                resolve(results.Payload)
            }
        })
    })
}
