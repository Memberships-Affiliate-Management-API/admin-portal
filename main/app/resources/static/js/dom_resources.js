/**
 * main application for system admin app for membership and affiliate api
 *
 *@__developer__ = "mobius-crypt"
 *@__email__ = "mobiusndou@gmail.com"
 *@__twitter__ = "@blueitserver"
 *@__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
 *@__github_profile__ = "https://github.com/freelancing-solutions/"
 *
 */

function return_dashboard_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */
    return `
    <div class="card">
        <div class="card-header">
            <h3 class="card-title"> Dashboard </h3>               
        </div>
        <div class="card-body">
            <!-- TODO add dashboard details here        -->
        </div>  
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>                           
    </div>           
    `
}



function return_organizations_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

    return `
        <div class="card">
            <div class="card-header">
                <h3 class="card-title"> Organizations </h3>               
            </div>
            <div class="card-body">            
            </div>   
            <div class="card-footer">
                <p class="card-text">{{ message }}</p>
            </div>         
        </div>    
    `
}



function return_users_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

    return `
    <div class="card">
        <div class="card-header">
            <h3 class="card-title"> Users </h3>               
        </div>
        <div class="card-body">
        
        </div>      
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>         
              
    </div>    
    
    `
}



function return_api_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

   return `
    <div class="card">
        <div class="card-header">
            <h3 class="card-title"> API Keys </h3>               
        </div>
        <div class="card-body">
        
        </div>          
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>         
          
    </div>    
   
   `
}



function return_affiliates_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

    return `
        <div class="card">
        <div class="card-header">
            <h3 class="card-title"> Affiliates </h3>               
        </div>
        <div class="card-body">
        
        </div>      
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>         
              
    </div>    

    `
}



function return_accounts_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

    return `
        <div class="card">
        <div class="card-header">
            <h3 class="card-title"> Accounts </h3>               
        </div>
        <div class="card-body">
        
        </div>           
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>         
         
    </div>    

    `
}



function return_help_desk_dom(){
    /**
     * returns a dom template to be compiled and populated using handlebars
     * @returns{string} handlebars template string
     */

    return `
        <div class="card">
        <div class="card-header">
            <h3 class="card-title"> Help Desk </h3>               
        </div>
        <div class="card-body">
        
        </div>   
        <div class="card-footer">
            <p class="card-text">{{ message }}</p>
        </div>         
                 
    </div>    

    `
}

