from .cog import Example

async def setup(bot):
    await bot.add_cog(Example(bot))

