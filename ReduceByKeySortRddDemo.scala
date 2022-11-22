package com.bigdata.spark.reducebykey_sort

import org.apache.spark.{SparkConf, SparkContext}

/**
 * @program: spark-api-demo
 * @description: 类作用描述
 * @author: 小毕
 * @company: 清华大学深圳研究生院
 * @create: 2019-09-02 18:00
 */
object ReduceByKeySortRddDemo {

  def main(args: Array[String]): Unit = {
    val conf=new SparkConf()
      .setAppName("MapFilterApp")
      .setMaster("local")
    val sc=new SparkContext(conf)
    val rdd1=sc.parallelize(List(("tom", 1), ("jerry", 3), ("kitty", 2),  ("shuke", 1)))
    val rdd2=sc.parallelize(List(("jerry", 2), ("tom", 3), ("shuke", 2), ("kitty", 5)))
    val rdd3=rdd1.union(rdd2)
    //按key进行聚合
    val rdd4=rdd3.reduceByKey(_+_)
    rdd4.collect.foreach(println(_))
    //按value的降序排序
    val rdd5=rdd4.map(t=>(t._2,t._1)).sortByKey(false).map(t=>(t._2,t._1))
    rdd5.collect.foreach(println)
  }

}
