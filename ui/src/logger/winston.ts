import { DEVELOPMENT } from "constants/enviournment";
import { DEBUG, ERROR, INFO } from "constants/log-level";

import winston, { Logger } from "winston";

const enumerateErrorFormat = winston.format(
  (info: winston.Logform.TransformableInfo) => {
    if (info instanceof Error) {
      Object.assign(info, { message: info.stack });
    }

    return info;
  },
);

export const getLogger = (): Logger => {
  const env = process.env.NODE_ENV;
  const prettyPrint = process.env.PRETTY_PRINT === "true";

  return winston.createLogger({
    level: env === DEVELOPMENT ? DEBUG : INFO,
    format: winston.format.combine(
      enumerateErrorFormat(),
      winston.format.json({ space: prettyPrint ? 2 : 0 }),
      env === DEVELOPMENT
        ? winston.format.colorize({
            all: prettyPrint,
          })
        : winston.format.uncolorize(),
      winston.format.timestamp(),
      winston.format.splat(),
    ),
    transports: [
      new winston.transports.Console({
        stderrLevels: [ERROR],
      }),
    ],
  });
};
