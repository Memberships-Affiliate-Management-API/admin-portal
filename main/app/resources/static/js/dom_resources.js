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
                <!-- insert a table of organizations here as contents -->
                <table class="table table-responsive">
                    <thead>
                        <tr>
                            <td>Organization Name</td>
                            <td>Affiliates </td>
                            <td>Total Paid </td>
                            <td>Total Users</td>
                            <td>Total Subscribers</td>
                            <td>Total Payments (Subscribers)</td>
                            <td>Home URL</td>                           
                        </tr>                    
                    </thead>
                    <tbody>                                        
                    </tbody>    
                    <tfoot>
                        <tr>
                            <td>Organization Name</td>
                            <td>Affiliates </td>
                            <td>Total Paid </td>
                            <td>Total Users</td>
                            <td>Total Subscribers</td>
                            <td>Total Payments (Subscribers)</td>
                            <td>Home URL</td>                           
                        </tr>                                        
                    </tfoot>            
                </table>      
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
        <table class="table table-responsive">
            <thead>
                <tr>
                    <td>Names</td>
                    <td>Surname</td>
                    <td>Cell</td>
                    <td>Email</td>
                    <td>Last Login</td>                
                    <td>Verified</td>
                    <td>Is Admin</td>
                </tr>            
            </thead>
            <tbody>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>            
            </tbody>
            <tfoot>
                <tr>
                    <td>Names</td>
                    <td>Surname</td>
                    <td>Cell</td>
                    <td>Email</td>
                    <td>Last Login</td>                
                    <td>Verified</td>
                    <td>Is Admin</td>
                </tr>                        
            </tfoot>
        </table>
        
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
            <table class="table table-responsive">
                <thead>
                    <tr>
                        <td>api key</td>
                        <td>uid</td>
                        <td>domain</td>
                        <td>is active</td>                    
                    </tr>                
                </thead>
                <tbody>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>                
                </tbody>
                <tfoot>
                        <td>api key</td>
                        <td>uid</td>
                        <td>domain</td>
                        <td>is active</td>                                    
                </tfoot>
            </table>
            
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
        <table>
            <thead>
                <tr>
                    <td>affiliate id</td>
                    <td>uid</td>
                    <td>Date Recruited</td>
                    <td>Total Recruits</td>
                    <td>is Active</td>                
                </tr>            
            </thead>        
            <tbody>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>            
            </tbody>
            <tfoot>
                <tr>
                    <td>affiliate id</td>
                    <td>uid</td>
                    <td>Date Recruited</td>
                    <td>Total Recruits</td>
                    <td>is Active</td>                
                </tr>                        
            </tfoot>            
        </table>
        
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
            <span class="card-text">Subscribers or members of this organization</span>       
        </div>
        <div class="card-body">
        <table class="table table-responsive">
            <thead>
                <tr>
                    <td>uid</td>
                    <td>plan_id</td>
                    <td>Payment Status</td>
                    <td>Date Created</td>
                    <td>Start Date</td>
                    <td>Payment Method</td>
                    <td>Is Active</td>
                </tr>            
            </thead>
        
        </table>
        
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

