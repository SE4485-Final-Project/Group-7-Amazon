exports.handler = async (event) => {

    if(event.queryStringParameters){
        
        if(event.queryStringParameters.first_num && event.queryStringParameters.second_num && event.queryStringParameters.operator){
            
            let result = 0
            const operator = event.queryStringParameters.operator 
            const first_num = parseInt(event.queryStringParameters.first_num)
            const second_num = parseInt(event.queryStringParameters.second_num)
            
            if(operator === 'add'){
                result = first_num + second_num
            }
            else if(operator === 'subtract'){
                result = first_num - second_num
            }
            
            const response = {
            statusCode: 200,
            body: JSON.stringify(`First num is: ${event.queryStringParameters.first_num}, 
            second num is: ${event.queryStringParameters.second_num}, operator is : ${operator}, result is: ${result}`),
            };
            
            return response
            
            }
            
            else{
                const response = {
                statusCode: 200,
                body: JSON.stringify(`Nothing to see here...`),
                };
                
                return response
            }
    }
    
    const response = {
    statusCode: 200,
    body: JSON.stringify('Hello from Lambda!'),
    };
    
    return response;
};
