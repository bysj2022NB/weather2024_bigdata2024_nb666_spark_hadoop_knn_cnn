package com.bigdata.storm.kafka.util;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

/**
 * @program: storm-kafka-api-demo
 * @description: redis工具类
 * @author: 小毕
 * @company: 清华大学深圳研究生院
 * @create: 2019-08-22 17:23
 */
public class JedisUtil {
    
    /*redis连接池*/
    private static JedisPool pool;
    
    /**
    *@Description: 返回redis连接池
    *@Param: 
    *@return: 
    *@Author: 小毕
    *@date: 2019/8/22 0022
    */
    public static JedisPool getPool(){
        if(pool==null){
            //创建jedis连接池配置
            JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();
            //最大连接数
            jedisPoolConfig.setMaxTotal(20);
            //最大空闲连接
            jedisPoolConfig.setMaxIdle(5);
            pool=new JedisPool(jedisPoolConfig,"node03.hadoop.com",6379,3000);
        }
        return pool;
    }

    public static Jedis getConnection(){
        return getPool().getResource();
    }

/*    public static void main(String[] args) {
        //System.out.println(getPool());
        //System.out.println(getConnection().set("hello","world"));
    }*/






    
    
}