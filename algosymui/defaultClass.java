import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.config.Configurator;

import java.math.BigDecimal;
import java.sql.SQLException;
import java.time.Instant;
import java.util.Arrays;
import java.util.Random;

public class TradingAlgorithmImpl implements TradingAlgorithm {
    private static Logger log = LogManager.getLogger(OrdersDAO.class);
    private OrdersDAO ordersBase;
    private CurrencyRates currencyRates;
    private static Random r = new Random(System.currentTimeMillis());

    public TradingAlgorithmImpl() throws SQLException {
        if (System.getProperty("framework.debug")!=null){
            Configurator.setLevel("TradingAlgorithmImpl",Level.DEBUG);
        }

        currencyRates = new CurrencyRates();
        ordersBase = new OrdersDAO(currencyRates);
    }

    public void receiveTick(Tick tick) throws TradingLogicException, SQLException {
        CurrencyRate currencyRate = currencyRates.updateAndReturnCurrentRate(tick.getCurrencyPair(),tick.getRate());
        log.debug(String.format("%s - %s: %s",
                Instant.ofEpochSecond(tick.getTimestamp()).toString(),
                tick.getCurrencyPair(),
                currencyRate.toString()));

        /* put you trading logic here */

        if (r.nextBoolean()) { // imitation of favourable conditions
            double stopLoss = 0.001 * r.nextDouble(); // imitation of user choice of stop-loss level
            double makeProfit = 0.001 * r.nextDouble(); // imitation of user choice of make-profit level

                Order o1 = new Order(currencyRate, tick.getCurrencyPair());
                if (Arrays.asList(tick.getCurrencyPair().split("/")).contains("RUB")) {
                    o1.buyNow()
                            .lot(50)
                            .stopLoss(tick.getRate().subtract(new BigDecimal(String.valueOf(stopLoss * 100))))
                            .makeProfit(tick.getRate().add(new BigDecimal(String.valueOf(makeProfit * 100))));
                } else {
                    o1.buyNow()
                            .lot(10)
                            .stopLoss(tick.getRate().subtract(new BigDecimal(String.valueOf(stopLoss))))
                            .makeProfit(tick.getRate().add(new BigDecimal(String.valueOf(makeProfit))));
                }
                ordersBase.put(o1);
        }

        ordersBase.executeOrders(tick.getCurrencyPair());
    }

    @Override
    public void evaluateResult() throws SQLException {
        System.out.println(ordersBase.evaluateWinLoss());
        ordersBase.clearDB();
    }

}
