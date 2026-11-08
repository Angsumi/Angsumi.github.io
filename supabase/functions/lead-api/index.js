import { createClient } from 'npm:@supabase/supabase-js@2';
import {createHandler} from './handler.mjs';
const env=key=>Deno.env.get(key);
const options={auth:{persistSession:false,autoRefreshToken:false}};
const db=createClient(env('SUPABASE_URL'),env('SUPABASE_SERVICE_ROLE_KEY'),options);
// Independent per-request Auth client avoids sharing a mutable user session between requests.
Deno.serve(async request=>createHandler({db,auth:createClient(env('SUPABASE_URL'),env('SUPABASE_ANON_KEY'),options),env})(request));
