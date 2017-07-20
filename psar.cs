cs


using System;
using System.Drawing;

using OpenQuant.API;
using OpenQuant.API.Indicators;
using OpenQuant.API.Plugins;

public class ParaSAR: UserIndicator
{
   
   
   public ParaSAR(BarSeries input) : base(input)
   {
      Name = "ParaSAR";
   }


   public override double Calculate(int index)
   {
      if (index > 1) {
            
         DateTime datetime1;
         DateTime datetime2;

         Double IAF = .02;
         Double MaxAF = .2;
         
         // Initialize Variables
         Double psar = Input[index, BarData.Close];
         Double prepsar = Input[index, BarData.Close];
         Double longFlag = 1;
         Double af = IAF;
         Double ep = Input[index, BarData.Low];
         Double hp = Input[index, BarData.High];
         Double lp = Input[index, BarData.Low];
         Double reverse = 0;

         datetime2 = DateTime.Now;
         datetime1 = datetime2.AddDays(-5);

         // 

         if (longFlag == 1) {
            psar = prepsar + af * (hp - prepsar);
            
         }
         else {
            psar = prepsar + af * (lp - prepsar);
            
         }

         reverse = 0;
         // Check for reversal

         if (longFlag == 1) {
            if (Input[index, BarData.Low] < psar) {
               longFlag = 0 ; 
               reverse = 1;    // reverse position to short
               psar = hp;      // SAR is High point in previous trade
               lp = Input[index, BarData.Low];
               af = IAF;
               return psar;
            }
         }
         else {
            if (Input[index, BarData.High] > psar) {
               longFlag = 1;
               reverse = 0;   // reverse position to long
               psar = lp;
               hp = Input[index, BarData.High];
               af = IAF;
               return psar;
            }
         }

         if (reverse == 0) {
            if (longFlag == 1) {
               if (Input[index, BarData.High] > hp) {
                  hp = Input[index, BarData.High];
                  af = af + IAF;
                  if( af > MaxAF) {
                     af = MaxAF;
                  }
               }
               if(Input[index-1, BarData.Low] < psar) {
                  psar = Input[index-1, BarData.Low];
                  return psar;
               }
               if(Input[index-2, BarData.Low] < psar) {
                  psar = Input[index-2, BarData.Low];
                  return psar;
               }
            }
            else {
               if (Input[index, BarData.Low] < lp) {
                  lp = Input[index, BarData.Low];
                  af = af + IAF;
                  if( af > MaxAF) {
                     af = MaxAF;
                  }
               }
               if(Input[index-1, BarData.High] > psar) {
                  psar = Input[index-1, BarData.High];
                  return psar;
               }
               if(Input[index-2, BarData.High] > psar) {
                  psar = Input[index-2, BarData.High];
                  return psar;
               }
            }
         }
      }
   }
}
   
public class MyStrategy : Strategy
{
   public override void OnStrategyStart()
   {
   }

   public override void OnBar(Bar bar)
   {
   }
}
